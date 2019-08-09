from bs4 import BeautifulSoup as bs
import requests
from bota import constant
from bota.web_scrap import scrap_constant
import re
from bota.utility.discord_display import cvt_dict_to_discord_pretty_text
import os


# Div class r-fluid line-graph sometimes different for others
r_fluid_list = ['r-10', 'r-20', 'r-30', 'r-40', 'r-50']


def get_rank_medal(player_soup):
    result = {}
    rank_info = player_soup.findAll(constant.ITEM_PLAYER_RANK_INFO_TAG[0], constant.ITEM_PLAYER_RANK_INFO_TAG[1])[0]
    rank_title = rank_info.attrs[constant.ITEM_KEYWORD_TITLE].lower()
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
    return result


def get_win_loss(soup):
    win_loss_info = soup.find('span', {'class': 'game-record'})
    wins = '0'
    loss = '0'
    abandons = '0'
    try:
        wins = win_loss_info.find('span', {'class': 'wins'}).string
        loss = win_loss_info.find('span', {'class': 'losses'}).string
        abandons = win_loss_info.find('span', {'class': 'abandons'}).string
    except Exception:
        pass
    return {'wins': wins, 'losses': loss, 'abandons': abandons}


def get_name(soup):
    header_info = soup.find('div', {'class': 'header-content-title'})
    name = header_info.find('h1').contents[0]
    return {'name': name}


def get_winrate(soup):
    header = soup.find('div', {'class': 'header-content-secondary'})
    win_rate_info = header.find_all('dl')[-1]
    win_rate = win_rate_info.find('dd').string
    return {'win_rate' :win_rate}


def get_most_played_heroes(soup, top=5):
    info = soup.find('div', {'class': 'r-table r-only-mobile-5 heroes-overview'})
    rows = info.find_all('div', {'class': 'r-row'})
    result_row = []
    for i, row in enumerate(rows, 1):
        if i > top:
            break
        hero_name = row.find('div', {'class': "r-none-mobile"}).contents[0].string
        others = None
        for r_n in  r_fluid_list:
            others = row.find_all('div', {'class': f'r-fluid {r_n} r-line-graph'})
            if len(others):
               break
        if others is None:
            continue
        total_matches = others[0].contents[1].contents[0]
        win_rate = others[1].contents[1].contents[0]
        kda = others[2].contents[1].contents[0]
        result_row.append({'hero': hero_name, 'matches': total_matches, 'win': win_rate, 'kda': kda})

    return {'most_played_heroes' : result_row}


def get_latest_match(soup, top=5):
    info = soup.find('div', {'class': 'r-table r-only-mobile-5 performances-overview'})
    rows = info.find_all('div', {'class': 'r-row'})
    results = []
    last_played = ''
    for i, row in enumerate(rows, 1):
        if i > top:
            break
        hero_name = row.find('a').contents[0].attrs['title']
        hero_name_split = hero_name.split()
        if len(hero_name) > 14 and len(hero_name_split) > 1:
            hero_name = hero_name_split[0][0].upper() + hero_name_split[1][0].upper()

        result = row.find('div', {'class': 'r-fluid r-175 r-text-only r-right r-match-result'})
        status = result.find('a').attrs['class'][0]
        status = status[0].upper()
        time = result.find('time').string
        if i == 1:
            last_played = time

        game_info = row.find('div', {'class': 'r-fluid r-175 r-text-only r-first'})
        game_type = game_info.find('div', {'class': 'r-body'}).contents[0]
        game_mode = game_info.find('div', {'class': 'subtext'}).string
        game_mode_split = game_mode.split()
        game_mode_short = [x[0] for x in game_mode_split]
        game_mode_short = ''.join(game_mode_short).upper()
        print(game_type)
        if len(str(game_type)) < 11:
            match_type = str(game_type)
            match_type = match_type.split()[0]
            match_type = 'Tourney' if match_type == 'Tournament' else match_type
        else:
            match_type = game_mode.split()[0]

        duration = row.find('div', {'class': 'r-fluid r-125 r-line-graph r-duration'})
        duration = duration.find('div', {'class': 'r-body'}).contents[0]

        kda = row.find_all('span', {'class': 'value'})
        kda = kda[0].string + '/' + kda[1].string + '/' + kda[2].string

        results.append({'hero': hero_name, 'status': status, 'type': match_type,
                        'duration': duration, 'kda': kda})

    return {'latest_match': results, 'last_play': last_played}


def pretty_profile_text_for_discord(json_data, spaces=18):
    final_string = ''
    for key_1, value in json_data.items():
        if value == '' or value is None:
            continue
        if type(value) != list:
            value = value.strip()
            final_string += f"{key_1.upper()}:"
            final_string += f"    **{value}**\n"
        else:

            if key_1 == 'latest_match':
                table = cvt_dict_to_discord_pretty_text(value, rename_keys={'duration': 'time', 'status':'w/l'}, spaces=15,
                                                               custom_space={'w/l':4, 'type': 8, 'time': 8,
                                                                             'kda':8, 'win': 8, 'matches': 9})
            else:
                table = cvt_dict_to_discord_pretty_text(value, rename_keys={'duration': 'time', 'status': 'w/l'},
                                                        spaces=17,
                                                        custom_space={'w/l': 5, 'type': 12, 'time': 6,
                                                                      'kda': 8, 'win': 8, 'matches': 9})
            final_string += f"**{key_1.replace('_', ' ').upper()}**\n"
            final_string += '```cs\n' + table + '```'
    return final_string


def get_medal_url(medal, rank=None):
    medals_url = 'https://raw.githubusercontent.com/bendangnuksung/bota/master/bota/data/medals_small/'

    if medal == 'uncalibrated':
        return medals_url + 'uncalibrated.png' + '?raw=true'
    if rank is not None:
        rank = int(rank)
        if rank <= 10:
            medal_name = constant.MEDAL_IMMORTAL_UNDER[10]
        elif rank <= 100:
            medal_name = constant.MEDAL_IMMORTAL_UNDER[100]
        else:
            medal_name = constant.MEDAL_IMMORTAL_UNDER[5000]
        return medals_url + medal_name + '?raw=true'
    else:
        medal_name, medal_no = medal.split()
        medal_no = constant.MEDAL_NUMBERING[medal_no]
        medal_name = medal_name + '-' + str(medal_no)
        medal_url = medals_url + (medal_name + '.png')
        return medal_url + '?raw=true'


def scrap_profile_info(profile_id):
    result = {}
    profile_id = str(profile_id)
    url = constant.PLAYER_URL_BASE + profile_id
    r = requests.get(url, headers=scrap_constant.browser_headers)
    if r.status_code != 200:
        return '', ''
    html = r.text
    soup = bs(html, 'html.parser')

    name_info = get_name(soup)
    result.update(name_info)

    win_loss_info = get_win_loss(soup)
    win_loss_info = {'Win-Loss-Abandon': win_loss_info['wins'] + '  -  ' + win_loss_info['losses'] + '  -  ' + win_loss_info['abandons']}
    result.update(win_loss_info)

    win_rate = get_winrate(soup)
    result.update(win_rate)

    medal_info = get_rank_medal(soup)
    result.update(medal_info)

    most_played_heros = get_most_played_heroes(soup)
    result.update(most_played_heros)

    latest_played_match = get_latest_match(soup)
    result.update(latest_played_match)

    string = pretty_profile_text_for_discord(result)

    medal = medal_info['medal']
    if medal_info['rank'] == '':
        medal = get_medal_url(medal)
    else:
        medal = get_medal_url(medal, rank=medal_info['rank'])

    string += f"**[DotaBuff]({url})**"

    return string, medal


if __name__ == '__main__':
    ids  = ['1234567890', '237445135','116585378', '425327377', '86753879', '86745912', '297066030', '46135920']
    for id in ids:
        r,link = (scrap_profile_info(id))
        print(r)
        print(link)
