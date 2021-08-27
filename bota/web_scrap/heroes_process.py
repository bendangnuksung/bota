import re, requests
from bota.web_scrap import scrap_constant
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import os
import difflib


def find_hero_name(hero):
    if scrap_constant.d2pt_to_dotabuff.get(hero) is not None:
        return True, scrap_constant.d2pt_to_dotabuff[hero]
    hero = hero.lower().strip()
    hero = re.sub('[^a-z- ]', '', hero)
    hero = hero.replace(' ', '-')
    close_matches = difflib.get_close_matches(hero, scrap_constant.heroes_names)
    if not len(close_matches):
        if hero in scrap_constant.heroes_name_alternative:
            hero_name = scrap_constant.heroes_name_alternative[hero]
            return True, hero_name
        return False, ''
    if hero == close_matches[0]:
        return True, close_matches[0]
    if hero in scrap_constant.heroes_name_alternative:
        hero_name = scrap_constant.heroes_name_alternative[hero]
        return True, hero_name
    return False, close_matches[0]


def reshape_heroes_result(results, section_name):
    results = np.reshape(np.array(results), (len(results) // scrap_constant.section_column_count[section_name],
                                             scrap_constant.section_column_count[section_name]))
    return results


def clean_header(section_headers, section_name):
    new_headers = []
    for header in section_headers:
        if header in scrap_constant.section_column_wanted[section_name]:
            new_headers.append(header)
    return new_headers


def get_heroes_section(section_name, html):
    section = re.search(f'<section><header>{section_name}.+?</section>', html).group()
    headers = re.findall(r'<th[^>]*>([^<]+)', section)
    rows = re.findall(r'<td>(?:<a[^>]*>)?([^<]+)', section)
    return rows, headers


def extract_counter_hero_from_html(html):
    soup = bs(html, 'html.parser')
    heroes = soup.find_all('td', {'class': 'cell-icon'})
    final_heroes = []
    for hero in heroes:
        h = hero.find('a')
        h = h.attrs['href']
        h = h.split('/')[-1]
        final_heroes.append(h)
    return final_heroes


def scrap_heroes_info(hero_name):
    url = os.path.join(scrap_constant.heroes_pre_url, hero_name)
    r = requests.get(url, headers=scrap_constant.browser_headers)
    html = r.text
    sections = scrap_constant.heroes_section_wanted
    panda_results = []
    for section_name in sections:
        results, section_header = get_heroes_section(section_name, html)
        results = reshape_heroes_result(results, section_name)
        section_header = clean_header(section_header, section_name)
        panda_result = pd.DataFrame(results, columns=section_header)
        panda_results.append(panda_result)
    return panda_results


def scrap_hero_counters(hero_name, is_counter=True):
    url = os.path.join(scrap_constant.heroes_pre_url, hero_name + "/counters")
    r = requests.get(url, headers=scrap_constant.browser_headers_mix)
    html = r.text
    heroes = extract_counter_hero_from_html(html)
    if is_counter == False:
        heroes = heroes[::-1]
    return heroes


def get_current_hero_trends():
    r = requests.get(scrap_constant.heroes_trend_url, headers=scrap_constant.browser_headers)
    html = r.text
    soup = bs(html, "html.parser")
    trend_list = [item[scrap_constant.trend_attribute_key_name]
                  for item in soup.find_all() if scrap_constant.trend_attribute_key_name in item.attrs]
    trend_list = np.array(trend_list)
    total_columns = len(scrap_constant.heroes_trend_columns)
    trend_list = np.reshape(trend_list, (len(trend_list) // total_columns, total_columns))
    panda_result = pd.DataFrame(trend_list, columns=scrap_constant.heroes_trend_columns)
    panda_result = panda_result.drop(scrap_constant.heros_unwanted_columns, axis=1)
    return panda_result


if __name__ == '__main__':
    # r = scrap_heroes_info('axe')
    all_heroes = scrap_constant.heroes_names
    for hero in all_heroes:
        print("*"*10)
        print(hero)
        r = scrap_hero_counters(hero)
        print(r)
    # r = find_hero_name('brood')
    # print(r)



