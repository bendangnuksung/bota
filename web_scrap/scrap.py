from web_scrap.heroes_process import get_current_hero_trends, find_hero_name, scrap_heroes_info
import pandas as pd
from utility import render_mpl_table, get_icon_path, is_file_old
from constant import CT_IMAGE_PATH, CT_IMAGE_UPDATE_TIME_THRESHOLD
import constant
import os
import cv2
from PIL import Image, ImageEnhance
import numpy as np


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


def add_border_to_image(im, bordersize=5, rgb=[45, 33, 31]):
    border = cv2.copyMakeBorder(im, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize,
                                borderType=cv2.BORDER_CONSTANT, value=rgb)
    return border


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
        y = y + ((i % constant.COUNTER_MAX_COLUMN) * image.shape[1]) +\
            ((i % constant.COUNTER_MAX_COLUMN) * constant.COUNTER_WIDTH_DIST)
        bg_image[x: x + image.shape[0], y: y + image.shape[1], :] = image
    return bg_image


def get_counter_hero(query):
    query = query.split()
    hero = ' '.join(query[1:])
    hero = hero.strip()
    found_hero, hero_name = find_hero_name(hero)
    if not found_hero:
        return False, hero_name, ''
    image_path = os.path.join(constant.COUNTER_HERO_IMAGE_PATH, hero_name + '.png')
    if not is_file_old(image_path, constant.COUNTER_HERO_UPDATE_TIME_THRESHOLD):
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


def get_good_against(query):
    query = query.split()
    hero = ' '.join(query[1:])
    hero = hero.strip()
    found_hero, hero_name = find_hero_name(hero)
    if not found_hero:
        return False, hero_name, ''
    image_path = os.path.join(constant.GOOD_HERO_IMAGE_PATH, hero_name + '.png')
    if not is_file_old(image_path, constant.COUNTER_HERO_UPDATE_TIME_THRESHOLD):
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


if __name__ == '__main__':
    print(get_counter_hero('!good ursa'))
    print(get_good_against('!good ursa'))

