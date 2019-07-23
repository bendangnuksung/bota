from bs4 import BeautifulSoup as bs
import requests
from web_scrap import scrap_constant
import constant
import utility
import numpy as np
import os
import re
import cv2
from image_processing import addImageWatermark, write_text, write_text_pil, add_border_to_image
import difflib


def display(img):
    import matplotlib.pyplot as plt
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.show()


def find_item(item):
    found_item = False
    item = item.lower().strip()
    item = re.sub('[^a-z- ]', '', item)
    item = item.replace(' ', '-')
    close_matches = difflib.get_close_matches(item, scrap_constant.ITEM_NAMES)
    if not len(close_matches):
        return found_item, ''
    if item == close_matches[0]:
        return True, close_matches[0]
    return False, close_matches[0]


def make_item_image(infos, hero_name):
    bg_image = cv2.imread(constant.ITEM_BACKGROUND_IMAGE)
    bg_image = cv2.resize(bg_image, (constant.ITEM_BACKGROUND_IMAGE_SHAPE[1], constant.ITEM_BACKGROUND_IMAGE_SHAPE[0]))
    hero_icon_image = cv2.imread(os.path.join(constant.ICON_PATH_BIG, hero_name + '.png'))
    hero_icon_image = add_border_to_image(hero_icon_image, rgb=[255, 255, 255])
    icon_h, icon_w, _ = hero_icon_image.shape
    bg_h, bg_w, _ = bg_image.shape
    new_x = 5
    new_y = 30
    bg_image[new_x: new_x + icon_h, new_y: new_y + icon_w, :] = hero_icon_image

    for i, info in enumerate(infos):
        medal = info['medal']
        rank = info['rank']

        medal_image_path = utility.get_medal_image_path(medal, rank)
        medal_image = cv2.imread(medal_image_path, -1)
        medal_image = cv2.resize(medal_image, (constant.MEDAL_SHAPE[1], constant.MEDAL_SHAPE[0]))
        X = constant.MEDAL_ITEM_X_Y[0]
        Y = constant.MEDAL_ITEM_X_Y[1]
        Y = Y + (i * constant.MEDAL_ITEM_HEIGHT_DIFF)

        # Add medals to bg
        bg_image = addImageWatermark(medal_image, bg_image, (X, Y))

        # write Rank in medals
        rank = str(rank)
        rank_position = (X + int(medal_image.shape[1] * constant.MEDAL_RANK_START_X_Y_PERCENTAGE[1]),
                         Y + int(medal_image.shape[0] * constant.MEDAL_RANK_START_X_Y_PERCENTAGE[0]))
        bg_image = write_text_pil(bg_image, rank, rank_position)

        # write other info to bg
        player_name = info['player_name'][:8]
        player_name_pos = (X + 200, Y + (medal_image.shape[0] // 3))
        bg_image = write_text_pil(bg_image, player_name, player_name_pos, size=25)

        player_id = info['player_id']
        player_id_pos = (X + 330, Y + (medal_image.shape[0] // 3))
        bg_image = write_text_pil(bg_image, player_id, player_id_pos, size=25)

        region = info['region']
        region_pos = (X + 480, Y + (medal_image.shape[0] // 3))
        bg_image = write_text_pil(bg_image, region, region_pos, size=25)

        # Write and add items
        for j, (time, raw_item_name) in enumerate(info['item_build'].items()):
            item_found, item_name = find_item(raw_item_name)
            item_icon_path = os.path.join(constant.ITEM_ICON_PATH, item_name + '.png')
            item_icon_image = cv2.imread(item_icon_path)
            item_icon_image = add_border_to_image(item_icon_image, rgb=[255, 255, 255], bordersize=3)
            item_icon_image = cv2.resize(item_icon_image, constant.ITEM_ICON_SHAPE)





    # display(bg_image)


def get_html_text(url):
    r = requests.get(url, headers=scrap_constant.browser_headers)
    html_text = r.text
    return html_text


def scrap_item_info(hero_name):
    final_result = []
    hero_url = constant.ITEM_URL.replace('<hero_name>', hero_name)
    html = get_html_text(hero_url)
    soup = bs(html, "html.parser")

    item_build_tag_list = soup.findAll(constant.ITEM_FIRST_STAGE_TAG[0], constant.ITEM_FIRST_STAGE_TAG[1])
    for item in item_build_tag_list:
        result = {}

        # Get player Name and ID
        player_tag = item.find_all(constant.ITEM_PLAYER_NAME_ID_TAG[0], constant.ITEM_PLAYER_NAME_ID_TAG[1])[0]
        for player in player_tag:
            result[constant.ITEM_KEYWORD_PLAYER_NAME] = player.string
            result[constant.ITEM_KEYWORD_PLAYER_ID]   = player.attrs['href'].split('/')[-1]
            break

        # Get item build by the Player
        item_builds = item.find_all(constant.ITEM_BUILD_TAG[0], constant.ITEM_BUILD_TAG[1])
        for div_tag in item_builds:
            time_tag = div_tag.find_all(constant.ITEM_BUILD_TIME_TAG[0], constant.ITEM_BUILD_TIME_TAG[1])
            item_tag = div_tag.find_all(constant.ITEM_BUILD_ITEM_TAG[0], constant.ITEM_BUILD_ITEM_TAG[1])
            item_build_dict = {}
            for itm, time in zip(item_tag, time_tag):
                item_build_dict[time.string] = itm.attrs[constant.ITEM_KEYWORD_TITLE]
            result[constant.ITEM_KEYWORD_ITEM_BUILD] = item_build_dict

        # Get Region
        region_info = item.find_all(constant.ITEM_REGION_FIRST_TAG[0], constant.ITEM_REGION_FIRST_TAG[1])
        for i, r in enumerate(region_info, 1):
            if i == 4:
                r = str(r).split('>')[-2]
                r = r.split('<')[0].strip()
                result[constant.ITEM_KEYWORD_REGION] = r
                break

        # Get Player Rank and Medal
        player_url = constant.DOTABUFF_PLAYER_URL + result[constant.ITEM_KEYWORD_PLAYER_ID]
        html = get_html_text(player_url)
        player_soup = bs(html, 'html.parser')
        rank_info = player_soup.findAll(constant.ITEM_PLAYER_RANK_INFO_TAG[0], constant.ITEM_PLAYER_RANK_INFO_TAG[1])[0]
        rank_title = rank_info.attrs[constant.ITEM_KEYWORD_TITLE].lower()
        if constant.ITEM_RANK_PRE_CHAR in rank_title:
            for i, char in enumerate(rank_title):
                if constant.ITEM_RANK_PRE_CHAR == char:
                    rank_info = rank_title[i + 1:]
                    rank_info = re.sub('[^0-9a-z ]+', '', rank_info)
                    rank, rank_medal = rank_info.split()
                    result[constant.ITEM_KEYWORD_RANK] = rank
                    result[constant.ITEM_KEYWORD_RANK_MEDAl] = rank_medal
        else:
            rank_medal = rank_title.replace('rank: ', '')
            result[constant.ITEM_KEYWORD_RANK] = 'None'
            result[constant.ITEM_KEYWORD_RANK_MEDAl] = rank_medal

        final_result.append(result)
    return final_result


if __name__ == '__main__':
    # make_item_image({}, 'anti-mage')
    # rs = scrap_item_info('anti-mage')
    # for r in rs:
    #     print(r)
    info = [{'player_name': 'Hope', 'player_id': '245655553', 'item_build': {'15:52': 'Battle Fury', '20:38': 'Manta Style', '26:18': 'Eye of Skadi', '31:13': 'Butterfly', '36:54': 'Abyssal Blade', '48:35': 'Assault Cuirass'}, 'region': 'SE Asia', 'rank': '285', 'medal': 'immortal'},
            {'player_name': 'haiz', 'player_id': '370966003', 'item_build': {'06:02': 'Wraith Band', '09:00': 'Power Treads', '16:16': 'Battle Fury', '21:38': 'Manta Style', '28:38': 'Abyssal Blade', '30:05': 'Eaglesong'}, 'region': 'US East', 'rank': '224', 'medal': 'immortal'},
            {'player_name': 'Zitraks Yana<3', 'player_id': '133558180', 'item_build': {'09:18': 'Power Treads', '15:22': 'Battle Fury', '19:39': 'Manta Style', '24:03': 'Eye of Skadi', '28:06': 'Butterfly', '32:31': 'Satanic'}, 'region': 'Europe West', 'rank': '59', 'medal': 'immortal'},
            {'player_name': 'qing', 'player_id': '196043199', 'item_build': {'10:52': 'Power Treads', '16:17': 'Battle Fury', '20:49': 'Manta Style', '25:15': 'Eye of Skadi', '29:55': 'Butterfly', '32:55': 'Skull Basher'}, 'region': 'Europe West', 'rank': '2453', 'medal': 'immortal'},
            {'player_name': 'Agressif', 'player_id': '130416036', 'item_build': {'15:47': 'Battle Fury', '21:21': 'Manta Style', '24:18': 'Eye of Skadi', '29:11': 'Butterfly', '36:07': 'Abyssal Blade', '37:19': 'Black King Bar'}, 'region': 'China', 'rank': '125', 'medal': 'immortal'}]
    # info =r
    make_item_image(info, 'anti-mage')
