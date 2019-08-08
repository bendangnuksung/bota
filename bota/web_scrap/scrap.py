from bota.image_processing import add_border_to_image
from bota.web_scrap.heroes_process import get_current_hero_trends, find_hero_name, scrap_heroes_info
import pandas as pd
from bota.utility.general import render_mpl_table, get_icon_path, is_file_old, crop_image
from bota.constant import CT_IMAGE_PATH, CT_IMAGE_UPDATE_TIME_THRESHOLD
from bota import constant
import os
import cv2
import numpy as np
from bota.web_scrap.web_screenshot import get_screenshot
from bota.web_scrap.items_process import scrap_item_info, make_item_image
from bota.web_scrap.profile_process import scrap_profile_info
from bota.web_scrap.reddit_process import scrap_reddit_dota
from bota.applications.steam_user import User
from bota.web_scrap.protracker_process import DotaProTracker


steam_user = User()
d2pt = DotaProTracker()


def round_df_digits(df):
    df = (df.astype(float).applymap('{:,.2f}'.format))
    return df


def get_current_trend():
    if not is_file_old(CT_IMAGE_PATH, CT_IMAGE_UPDATE_TIME_THRESHOLD):
        return CT_IMAGE_PATH

    current_trend_dataframe = get_current_hero_trends()
    current_trend_dataframe = current_trend_dataframe[:10]
    hero_name_df = current_trend_dataframe[current_trend_dataframe.columns[0]]
    numeric_df = current_trend_dataframe[current_trend_dataframe.columns[1:]]
    numeric_df = round_df_digits(numeric_df)
    heroes_list = hero_name_df.values.tolist()
    icon_path_list = get_icon_path(heroes_list)
    current_trend_dataframe = pd.concat([hero_name_df, numeric_df], axis=1)

    title = 'Current Heroes Trend \n\nWR: Win Rate                              PR: Pick Rate'
    image_path = render_mpl_table(current_trend_dataframe, icon_list=icon_path_list, header_columns=0, col_width=2.6,
                             title=title, font_size=20)
    return image_path


def make_hero_images(main_hero_image_path, heroes_image_path, bg_path):
    bg_image = cv2.imread(bg_path)
    bg_image = cv2.resize(bg_image, (constant.COUNTER_BG_SHAPE[1], constant.COUNTER_BG_SHAPE[0]))
    main_hero_image = cv2.imread(main_hero_image_path)
    X, Y = constant.COUNTER_MAIN_HERO_COORDS
    bg_image[X: X + main_hero_image.shape[0], Y: Y + main_hero_image.shape[1], :] = main_hero_image
    for i, path in enumerate(heroes_image_path):
        image = cv2.imread(path)
        image = cv2.resize(image, (constant.COUNTER_ICON_SHAPE[1], constant.COUNTER_ICON_SHAPE[0]))
        image = add_border_to_image(image)
        x, y = constant.COUNTER_START_COORDS
        x = x + ((i // constant.COUNTER_MAX_COLUMN) * constant.COUNTER_HEIGHT_DIST)
        y = y + ((i % constant.COUNTER_MAX_COLUMN) * image.shape[1]) + \
            ((i % constant.COUNTER_MAX_COLUMN) * constant.COUNTER_WIDTH_DIST)
        bg_image[x: x + image.shape[0], y: y + image.shape[1], :] = image
    return bg_image


def get_counter_hero(query, hero=None, early_update=False):
    if hero is None:
        query = query.split()
        hero = ' '.join(query[1:])
        hero = hero.strip()
    found_hero, hero_name = find_hero_name(hero)
    if not found_hero:
        return False, hero_name, ''
    image_path = os.path.join(constant.COUNTER_HERO_IMAGE_PATH, hero_name + '.png')

    threshold_update_time = constant.COUNTER_HERO_UPDATE_TIME_THRESHOLD
    if early_update:
        threshold_update_time = threshold_update_time - constant.EARLY_BY
    if not is_file_old(image_path, threshold_update_time):
        return True, hero_name, image_path

    hero_info = scrap_heroes_info(hero_name)
    counter_info = hero_info[0]
    counter_heroes = counter_info['Hero']
    counter_heroes_list = list(counter_heroes)
    counter_heroes_image_path = get_icon_path(counter_heroes_list, icon_size='big')
    hero_image_path = get_icon_path([hero_name], icon_size='big')[0]
    image = make_hero_images(hero_image_path, counter_heroes_image_path, constant.COUNTER_BG_IMAGE_PATH)
    cv2.imwrite(image_path, image)
    return True, hero_name, image_path


def get_good_against(query, hero=None, early_update=False):
    if hero is None:
        query = query.split()
        hero = ' '.join(query[1:])
        hero = hero.strip()
    found_hero, hero_name = find_hero_name(hero)
    if not found_hero:
        return False, hero_name, ''
    image_path = os.path.join(constant.GOOD_HERO_IMAGE_PATH, hero_name + '.png')

    threshold_update_time = constant.GOOD_HERO_UPDATE_TIME_THRESHOLD
    if early_update:
        threshold_update_time = threshold_update_time - constant.EARLY_BY
    if not is_file_old(image_path, threshold_update_time):
        return True, hero_name, image_path

    hero_info = scrap_heroes_info(hero_name)
    good_against_info = hero_info[1]
    good_against_heroes = good_against_info['Hero']
    good_against_heroes_list = list(good_against_heroes)
    good_against_heroes_image_path = get_icon_path(good_against_heroes_list, icon_size='big')
    hero_image_path = get_icon_path([hero_name], icon_size='big')[0]
    image = make_hero_images(hero_image_path, good_against_heroes_image_path, constant.GOOD_BG_IMAGE_PATH)
    cv2.imwrite(image_path, image)
    return True, hero_name, image_path


async def get_skill_build(query, hero=None, early_update=False):
    if hero is None:
        query = query.split()
        hero = ' '.join(query[1:])
        hero = hero.strip()
    found_hero, hero_name = find_hero_name(hero)
    if not found_hero:
        return False, hero_name, ''

    guide_image_path = os.path.join(constant.GUIDE_SAVE_PATH, hero_name + '.jpg')

    threshold_update_time = constant.GUIDE_THRESHOLD_IMAGE_UPDATE
    if early_update:
        threshold_update_time = threshold_update_time - constant.EARLY_BY
    if not is_file_old(guide_image_path, threshold_update_time):
        return True, hero_name, guide_image_path

    url = constant.GUIDE_URL.replace('<hero_name>', hero_name)

    talent_filename = hero + '_talent.jpg'
    talent_screenshot_path = os.path.join(constant.TEMP_IMAGE_PATH, talent_filename)
    await get_screenshot(constant.TALENT_SELECTOR, url, talent_screenshot_path)

    skill_filename = hero + '_skill.jpg'
    skill_screenshot_path = os.path.join(constant.TEMP_IMAGE_PATH, skill_filename)

    await get_screenshot(constant.SKILL_SELECTOR, url, skill_screenshot_path)

    talent_image = cv2.imread(talent_screenshot_path)
    talent_crop = crop_image(talent_image, constant.TALENT_CROP_COORDS)

    skill_image = cv2.imread(skill_screenshot_path)
    skill_crop = crop_image(skill_image, constant.SKILL_CROP_COORDS)

    hero_icon_path = os.path.join(constant.ICON_PATH_BIG, hero_name + '.png')
    hero_icon = cv2.imread(hero_icon_path)
    background_image = cv2.imread(constant.GUIDE_BACKGROUND_PATH)
    background_image = cv2.resize(background_image, (
    constant.GUIDE_BACKGROUND_SHAPE[1], constant.GUIDE_BACKGROUND_SHAPE[0]))
    background_image[constant.GUIDE_HERO_ICON_X_Y[0]: constant.GUIDE_HERO_ICON_X_Y[0] + hero_icon.shape[0],
    constant.GUIDE_HERO_ICON_X_Y[1]: constant.GUIDE_HERO_ICON_X_Y[1] + hero_icon.shape[1]] = hero_icon
    background_image = add_border_to_image(background_image, bordersize=10, rgb=[0, 0, 0])
    background_image = cv2.resize(background_image,
                                  (constant.GUIDE_BACKGROUND_SHAPE[1], constant.GUIDE_BACKGROUND_SHAPE[0]))
    final_image = np.concatenate([talent_crop, background_image, skill_crop], axis=0)
    cv2.imwrite(guide_image_path, final_image)
    return True, hero_name, guide_image_path


def get_item_build(query, hero=None, early_update=False):
    if hero is None:
        query = query.split()
        hero = ' '.join(query[1:])
        hero = hero.strip()
    found_hero, hero_name = find_hero_name(hero)
    if not found_hero:
        return False, hero_name, ''

    item_build_path = os.path.join(constant.ITEM_IMAGE_PATH, hero_name + '.jpg')

    threshold_update_time = constant.ITEM_THRESHOLD_UPDATE
    if early_update:
        threshold_update_time = threshold_update_time - constant.EARLY_BY
    if not is_file_old(item_build_path, threshold_update_time):
        return True, hero_name, item_build_path

    item_build_info = scrap_item_info(hero_name)
    item_image = make_item_image(item_build_info, hero_name)
    cv2.imwrite(item_build_path, item_image, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
    return True, hero_name, item_build_path


def is_id(id):
    flag = False
    try:
        test = int(id)
        flag = True
    except Exception:
        pass
    return flag


def get_profile(query):
    query = query.split()
    id = ' '.join(query[1:])
    id = id.strip()

    if is_id(id):
        profile_info_string = scrap_profile_info(id)
    else:
        user_name = id
        flag, id = steam_user.get_id(user_name)
        if not flag:
            return False, user_name, 2, ''
        profile_info_string = scrap_profile_info(id)
        return True, id, 2, profile_info_string
    if profile_info_string == '':
        return False, id, 1, ''
    return True, id, 1, profile_info_string


def save_id(query):
    query = query.split()
    user_name = query[1].strip()
    id = query[2].strip()
    flag, status = steam_user.add_user(user_name, id)
    return user_name, id, flag, status


def get_reddit(query):
    query = query.split()
    mode = constant.REDDIT_DEFAULT_MODE
    top = constant.REDDIT_DEFAULT_TOP
    if len(query) > 1:
        user_given_mode = query[1]
        # get modes from user if provided
        if user_given_mode in constant.REDDIT_SORT_BY:
            mode = user_given_mode
        # Get top(n) from user if provided
        if len(query) > 2:
            if query[2].isdigit():
                top = int(query[2])
    result = scrap_reddit_dota(sort_by=mode, top=top)
    return result, mode


def get_protracker_hero(query):
    query = query.split()
    hero = ' '.join(query[1:])
    hero = hero.strip()
    found_hero, hero_name = find_hero_name(hero)
    if not found_hero:
        return False, hero_name, ''

    result = d2pt.get_hero_details_from_d2pt(hero_name)
    icon_path = get_icon_path([hero_name], icon_size='big')[0]
    return True, hero_name, result, icon_path


if __name__ == '__main__':
    print(get_reddit('!reddit top'))
    exit()
    # print(save_id('!save sam 297066030'))
    print(get_profile('!profile david'))
    exit()
    # print(get_counter_hero('!good ursa'))
    # print(get_good_against('!good ursa'))
    import asyncio
    print(asyncio.get_event_loop().run_until_complete(get_skill_build('!good witch doctor')))
    # print(get_skill_build('!good witch doctor'))
    print(get_item_build('!good ursa'))