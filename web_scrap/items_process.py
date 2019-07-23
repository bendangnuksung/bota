from bs4 import BeautifulSoup as bs
import requests
from web_scrap import scrap_constant
import constant
import numpy as np
import os
import re


def get_html_text(url):
    r = requests.get(url, headers=scrap_constant.browser_headers)
    html_text = r.text
    return html_text


def get_item_build_info(hero_name):
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
    rs = get_item_build_info('anti-mage')
    for r in rs:
        print(r)
