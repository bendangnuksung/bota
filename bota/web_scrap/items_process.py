from bs4 import BeautifulSoup as bs
import urllib.request
from bota.utility.general import get_html_text
from bota.web_scrap import scrap_constant
from bota import constant
from bota.utility import general
import os
import re
import cv2
from bota.image_processing import addImageWatermark, write_text_pil, add_border_to_image
import difflib
import requests
import shutil
from bota.web_scrap.screenshot_and_template_matching import get_html_using_vpn, destroy_sel_driver


def display(img):
    import matplotlib.pyplot as plt
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.show()


def find_close_item(item):
    close_matches = difflib.get_close_matches(item, scrap_constant.ITEM_NAMES)
    if not len(close_matches):
        return False, ''
    if item == close_matches[0]:
        return True, close_matches[0]
    return False, close_matches[0]


def find_item(item):
    item = item.lower().strip()
    item = re.sub('[^a-z-0-9 ]', '', item)
    item = item.replace(' ', '-')
    item = item.rstrip('-')

    found_item, close_match = find_close_item(item)
    if not found_item:
        download_item_image(item)
    found_item, close_match = find_close_item(item)

    return found_item, close_match


def download_image(url, save_path):
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)\
            AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'}
    r = requests.get(url, stream=True, headers=header)
    r.raw.decode_content = True
    with open(save_path, 'wb') as f:
        shutil.copyfileobj(r.raw, f)


def download_item_image(item):
    item = item + '.jpg'
    url = constant.DOTABUFF_ITEM_IMAGE_URL + item
    save_path = os.path.join(constant.REPO_PATH, constant.ITEM_ICON_PATH)
    save_path = os.path.join(save_path, item)
    try:
        download_image(url, save_path)
        # urllib.request.urlretrieve(url, save_path)
        image = cv2.imread(save_path)
        new_save_path = save_path.replace('.jpg', '.png')
        cv2.imwrite(new_save_path, image)
        os.remove(save_path)
    except Exception as e:
        print("Failed Downloading item image: ", item, e)


def make_item_image(infos, hero_name):
    bg_image = cv2.imread(constant.ITEM_BACKGROUND_IMAGE)
    bg_image = cv2.resize(bg_image, (constant.ITEM_BACKGROUND_IMAGE_SHAPE[1], constant.ITEM_BACKGROUND_IMAGE_SHAPE[0]))
    hero_icon_image = cv2.imread(os.path.join(constant.ICON_PATH_BIG, hero_name + '.png'))
    hero_icon_image = add_border_to_image(hero_icon_image, rgb=[255, 255, 255])
    icon_h, icon_w, _ = hero_icon_image.shape
    bg_h, bg_w, _ = bg_image.shape
    hero_icon_x = constant.ITEM_HERO_ICON_PLACEMENT_TOP
    hero_icon_y = constant.ITEM_HERO_ICON_PLACEMENT_LEFT
    bg_image[hero_icon_x: hero_icon_x + icon_h, hero_icon_y: hero_icon_y + icon_w, :] = hero_icon_image

    for i, info in enumerate(infos):
        medal = info[constant.ITEM_KEYWORD_RANK_MEDAl]
        rank = info[constant.ITEM_KEYWORD_RANK]
        try:
            medal_image_path = general.get_medal_image_path(medal, rank)
        except Exception as e:
            print(e)
            continue

        # Top players should be either immortal or divine medals if not skip it
        flag_divine_immortal_medal = False
        for wanted_medal in constant.ITEM_TOP_PLAYERS_MEDALS:
            if wanted_medal in medal:
                flag_divine_immortal_medal = True
                break
        if not flag_divine_immortal_medal:
            continue

        medal_image = cv2.imread(medal_image_path, -1)
        medal_image = cv2.resize(medal_image, (constant.MEDAL_SHAPE[1], constant.MEDAL_SHAPE[0]))
        X = constant.MEDAL_ITEM_X_Y[0]
        Y = constant.MEDAL_ITEM_X_Y[1]
        Y = Y + (i * constant.MEDAL_ITEM_HEIGHT_DIFF)

        # Add medals to bg
        bg_image = addImageWatermark(medal_image, bg_image, (X, Y))

        # write Rank in medals
        rank = str(rank)
        if rank != '' and rank is not None:
            rank_position = (X + int(medal_image.shape[1] * constant.MEDAL_RANK_START_X_Y_PERCENTAGE[1]),
                             Y + int(medal_image.shape[0] * constant.MEDAL_RANK_START_X_Y_PERCENTAGE[0]))
            bg_image = write_text_pil(bg_image, rank, rank_position)

        # write other info to bg
        player_name = info[constant.ITEM_KEYWORD_PLAYER_NAME][:constant.MAX_CHAR_PLAYER_NAME]
        player_name_pos = (X + constant.PLAYER_NAME_START_LEFT, Y + (medal_image.shape[0] // 3))
        bg_image = write_text_pil(bg_image, player_name, player_name_pos, size=constant.PLAYER_NAME_FONT_SIZE)

        match_id = info[constant.ITEM_KEYWORD_MATCH_ID]
        match_id_pos = (X + constant.PLAYER_MATCH_ID_START_LEFT, Y + (medal_image.shape[0] // 3))
        bg_image = write_text_pil(bg_image, match_id, match_id_pos, size=constant.MATCH_ID_FONT_SIZE)

        region = info[constant.ITEM_KEYWORD_REGION][:constant.MAX_CHAR_REGION]
        region_pos = (X + constant.REGION_START_LEFT, Y + (medal_image.shape[0] // 3))
        bg_image = write_text_pil(bg_image, region, region_pos, size=constant.REGION_FONT_SIZE)

        # Write and add items
        for j, (time, raw_item_name) in enumerate(info[constant.ITEM_KEYWORD_ITEM_BUILD].items()):
            # icon
            if j + 1 > constant.MAX_ITEM:
                break
            item_found, item_name = find_item(raw_item_name)
            item_icon_path = os.path.join(constant.ITEM_ICON_PATH, item_name + '.png')
            item_icon_image = cv2.imread(item_icon_path)
            item_icon_image = add_border_to_image(item_icon_image, rgb=[255, 255, 255], bordersize=3)
            item_icon_image = cv2.resize(item_icon_image, constant.ITEM_ICON_SHAPE)
            item_y = Y + (medal_image.shape[0] // 6)
            item_x = X + constant.ITEM_START_LEFT + (j * (item_icon_image.shape[1]))
            bg_image[item_y: item_y + item_icon_image.shape[0],
                     item_x: item_x + item_icon_image.shape[1]] = item_icon_image

            # time
            item_time_y = Y + constant.TIME_START_TOP
            item_time_x = item_x
            bg_image = write_text_pil(bg_image, time, (item_time_x, item_time_y), size=constant.TIME_FONT_SIZE)

        # Write and add starting items
        j = 0
        for raw_item_name in info['starting_items']:
            # icon
            if raw_item_name == 'town-portal-scroll':
                continue
            if j + 1 > constant.MAX_ITEM:
                break
            item_found, item_name = find_item(raw_item_name)
            item_icon_path = os.path.join(constant.ITEM_ICON_PATH, item_name + '.png')
            item_icon_image = cv2.imread(item_icon_path)
            item_icon_image = add_border_to_image(item_icon_image, rgb=[255, 255, 255], bordersize=1)
            item_icon_image = cv2.resize(item_icon_image, constant.ITEM_ICON_SHAPE)
            item_y = Y + (medal_image.shape[0] // 6)
            item_x = X + (constant.ITEM_START_LEFT + 435) + (j * (item_icon_image.shape[1]))
            bg_image[item_y: item_y + item_icon_image.shape[0],
            item_x: item_x + item_icon_image.shape[1]] = item_icon_image

            # time
            item_time_y = Y + constant.TIME_START_TOP
            item_time_x = item_x
            bg_image = write_text_pil(bg_image, '', (item_time_x, item_time_y), size=constant.TIME_FONT_SIZE)
            j += 1

    new_height, new_width = int(bg_image.shape[0] * 0.84), int(bg_image.shape[1] * 0.84) # resizing for image size
    bg_image = cv2.resize(bg_image, (new_width, new_height))
    return bg_image
    # display(bg_image)


def scrap_item_info(hero_name):
    final_result = []
    hero_url = constant.ITEM_URL.replace('<hero_name>', hero_name)
    html = get_html_text(hero_url)
    soup = bs(html, "html.parser")

    item_build_tag_list = soup.findAll(constant.ITEM_FIRST_STAGE_TAG[0], constant.ITEM_FIRST_STAGE_TAG[1])
    if not len(item_build_tag_list):
        html = get_html_using_vpn(hero_url)
        soup = bs(html, "html.parser")
        item_build_tag_list = soup.findAll(constant.ITEM_FIRST_STAGE_TAG[0], constant.ITEM_FIRST_STAGE_TAG[1])
    # else:
    #     destroy_sel_driver()

    for item in item_build_tag_list:
        result = {}

        # Get player Name and ID
        player_tag = item.find_all(constant.ITEM_PLAYER_NAME_ID_TAG[0], constant.ITEM_PLAYER_NAME_ID_TAG[1])[0]
        for player in player_tag:
            result[constant.ITEM_KEYWORD_PLAYER_NAME] = player.string
            result[constant.ITEM_KEYWORD_PLAYER_ID]   = player.attrs['href'].split('/')[-1]
            break

        # Get Match ID
        match_tag = item.find_all(constant.ITEM_MATCH_ID_TAG[0], constant.ITEM_MATCH_ID_TAG[1])[0]
        match_id = match_tag.attrs['href']
        match_id = match_id.split('?')[0]
        match_id = match_id.split('/')[-1]
        result[constant.ITEM_KEYWORD_MATCH_ID] = match_id

        # Get item build by the Player
        item_builds = item.find_all(constant.ITEM_BUILD_TAG[0], constant.ITEM_BUILD_TAG[1])
        for div_tag in item_builds:
            time_tag = div_tag.find_all(constant.ITEM_BUILD_TIME_TAG[0], constant.ITEM_BUILD_TIME_TAG[1])
            item_tag = div_tag.find_all(constant.ITEM_BUILD_ITEM_TAG[0], constant.ITEM_BUILD_ITEM_TAG[1])

            item_build_dict = {}
            c = '.'
            for i in range(len(item_tag)):
                if i < len(time_tag):
                    item_name = item_tag[i].attrs[constant.ITEM_KEYWORD_TITLE]
                    if item_name == '':
                        item_name = item_tag[i].attrs[constant.ITEM_KEYWORD_OLD_TITLE]
                    item_build_dict[time_tag[i].string] = item_name
                else:
                    item_name = item_tag[i].attrs[constant.ITEM_KEYWORD_TITLE]
                    if item_name == '':
                        item_name = item_tag[i].attrs[constant.ITEM_KEYWORD_OLD_TITLE]
                    item_build_dict[c] = item_name
                    c += '.'
            # for itm, time in zip(item_tag, time_tag):
            #     item_build_dict[time.string] = itm.attrs[constant.ITEM_KEYWORD_TITLE]
            result[constant.ITEM_KEYWORD_ITEM_BUILD] = item_build_dict

        # Starting items:
        result['starting_items'] = []
        starting_items = item.find_all('div', {"class": "kv r-none-mobile"})[0]
        for div_tag in starting_items:
            item_name = div_tag.find('a')
            if item_name is None:
                continue
            item_name = item_name.attrs['href']
            item_name = os.path.basename(item_name)
            result['starting_items'].append(item_name)

        # Get Region
        region_info = item.find_all(constant.ITEM_REGION_FIRST_TAG[0], constant.ITEM_REGION_FIRST_TAG[1])
        for i, r in enumerate(region_info, 1):
            if i == len(region_info) - 2:
                r = str(r).split('>')[-2]
                r = r.split('<')[0].strip()
                result[constant.ITEM_KEYWORD_REGION] = r
                break

        # Get Player Rank and Medal
        player_url = constant.DOTABUFF_PLAYER_URL + result[constant.ITEM_KEYWORD_PLAYER_ID]

        got_data_flag = False
        rank_title = None
        try:
            html = get_html_text(player_url)
            player_soup = bs(html, 'html.parser')
            rank_info = player_soup.findAll(constant.ITEM_PLAYER_RANK_INFO_TAG[0], constant.ITEM_PLAYER_RANK_INFO_TAG[1])[0]
            rank_title = rank_info.attrs[constant.ITEM_KEYWORD_TITLE].lower()
            if rank_title == '':
                rank_title = rank_info.attrs[constant.ITEM_KEYWORD_OLD_TITLE].lower()
            got_data_flag = True
        except:
            got_data_flag = False
        finally:
            if not got_data_flag:
                html = get_html_using_vpn(player_url)
                player_soup = bs(html, 'html.parser')
                rank_info = player_soup.findAll(constant.ITEM_PLAYER_RANK_INFO_TAG[0], constant.ITEM_PLAYER_RANK_INFO_TAG[1])[0]
                rank_title = rank_info.attrs[constant.ITEM_KEYWORD_TITLE].lower()
                if rank_title == '':
                    rank_title = rank_info.attrs[constant.ITEM_KEYWORD_OLD_TITLE].lower()

        if constant.ITEM_RANK_PRE_CHAR in rank_title:
            for i, char in enumerate(rank_title):
                if constant.ITEM_RANK_PRE_CHAR == char:
                    rank_info = rank_title[i + 1:]
                    rank_info = re.sub('[^0-9a-z ]+', '', rank_info)
                    rank_info_list = rank_info.split()
                    rank = rank_info_list[0]
                    rank_medal = ' '.join(rank_info_list[1:])
                    result[constant.ITEM_KEYWORD_RANK] = rank
                    result[constant.ITEM_KEYWORD_RANK_MEDAl] = rank_medal
        else:
            rank_medal = rank_title.replace('rank: ', '')
            result[constant.ITEM_KEYWORD_RANK] = ''
            result[constant.ITEM_KEYWORD_RANK_MEDAl] = rank_medal

        final_result.append(result)
    return final_result


if __name__ == '__main__':
    rs = scrap_item_info('lifestealer')
    for r in rs:
        print(r)
    # rs = [{'player_name': 'Hope', 'player_id': '245655553', 'item_build': {'15:52': 'Battle Fury', '20:38': 'Manta Style', '26:18': 'Eye of Skadi', '31:13': 'Butterfly', '36:54': 'Abyssal Blade', '48:35': 'Assault Cuirass'}, 'region': 'SE Asia', 'rank': '20', 'medal': 'ancient vii'},
    #         {'player_name': 'haiz', 'player_id': '370966003', 'item_build': {'06:02': 'Wraith Band', '09:00': 'Power Treads', '16:16': 'Battle Fury', '21:38': 'Manta Style', '28:38': 'Abyssal Blade', '30:05': 'Eaglesong'}, 'region': 'US East', 'rank': '', 'medal': 'legend 3'},
    #         {'player_name': 'Zitraks Yana<3', 'player_id': '133558180', 'item_build': {'09:18': 'Power Treads', '15:22': 'Battle Fury', '19:39': 'Manta Style', '24:03': 'Eye of Skadi', '28:06': 'Butterfly', '32:31': 'Satanic'}, 'region': 'Europe West', 'rank': '59', 'medal': 'immortal'},
    #         {'player_name': 'qing', 'player_id': '196043199', 'item_build': {'10:52': 'Power Treads', '16:17': 'Battle Fury', '20:49': 'Manta Style', '25:15': 'Eye of Skadi', '29:55': 'Butterfly', '32:55': 'Skull Basher'}, 'region': 'Europe West', 'rank': '2453', 'medal': 'immortal'},
    #         {'player_name': 'Agressif', 'player_id': '130416036', 'item_build': {'15:47': 'Battle Fury', '21:21': 'Manta Style', '24:18': 'Eye of Skadi', '29:11': 'Butterfly', '36:07': 'Abyssal Blade', '37:19': 'Black King Bar'}, 'region': 'China', 'rank': '125', 'medal': 'immortal'}]
    info = rs
    # print(info)
    image = make_item_image(info, 'pudge')
    display(image)
