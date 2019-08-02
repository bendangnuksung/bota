from bs4 import BeautifulSoup as bs
import requests
from bota import constant
from bota.web_scrap import scrap_constant
import re


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
    wins = win_loss_info.find('span', {'class': 'wins'}).string
    loss = win_loss_info.find('span', {'class': 'losses'}).string
    abandons = win_loss_info.find('span', {'class': 'abandons'}).string
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
        others = row.find_all('div', {'class': 'r-fluid r-10 r-line-graph'})
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

        result = row.find('div', {'class': 'r-fluid r-175 r-text-only r-right r-match-result'})
        status = result.find('a').attrs['class'][0]
        time = result.find('time').string
        if i == 1:
            last_played = time

        game_info = row.find('div', {'class': 'r-fluid r-175 r-text-only r-first'})
        game_type = game_info.find('div', {'class': 'r-body'}).contents[0]
        game_mode = game_info.find('div', {'class': 'subtext'}).string
        game_mode_split = game_mode.split()
        game_mode_short = [x[0] for x in game_mode_split]
        game_mode_short = ''.join(game_mode_short).upper()
        if len(str(game_type)) < 15:
            match_type = str(game_type) + '-' + game_mode_short
        else:
            match_type = game_mode

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
            final_string += f"**{key_1.upper()}:**"
            final_string += f"    {value}\n"
        else:
            temp_string = ''
            header_position = []
            header_name = []
            for i, dictionary in enumerate(value):
                temp_string += f"{i + 1}. "
                for j, (key_2, value) in enumerate(dictionary.items()):
                    # For 'hero name' allocatin the same number of space
                    # very bad practice of aligning for display purpose
                    if i == 0:
                        header_position.append(len(temp_string))
                        header_name.append(key_2)
                    if j == 0:
                        temp_val = f"{value}        "
                        remain_space = spaces - len(temp_val)
                        if remain_space > 0:
                            temp_string += temp_val + (' '*remain_space)
                        else:
                            temp_string += temp_val[:spaces]
                    elif i != 0:
                        current_len = header_position[j] - len(temp_string.split('\n')[-1])
                        if current_len < 0:
                            temp_string = temp_string[:current_len]
                            temp_string += f"{value}        "
                        else:
                            temp_string += ' ' * current_len + f"{value}        "
                    else:
                        temp_string += f"{value}        "
                temp_string += "\n"
            temp_header_str = ['*']*150
            for position, header in zip(header_position, header_name):
                # print(position, position + len(header))
                temp_header_str[position:position + len(header)] = header.upper()
            temp_header_str = ''.join(temp_header_str)
            temp_header_str = temp_header_str.replace('*', ' ')
            temp_header_str = temp_header_str.rstrip()
            final_string += f"**{key_1.replace('_', ' ').upper()}**\n"
            final_string += f"```glsl\n{temp_header_str}\n{temp_string}```\n"
    return final_string


def scrap_profile_info(profile_id):
    result = {}
    profile_id = str(profile_id)
    url = constant.PLAYER_URL_BASE + profile_id
    r = requests.get(url, headers=scrap_constant.browser_headers)
    if r.status_code != 200:
        return ''
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

    result['dotabuff'] = url

    most_played_heros = get_most_played_heroes(soup)
    result.update(most_played_heros)

    latest_played_match = get_latest_match(soup)
    result.update(latest_played_match)

    string = pretty_profile_text_for_discord(result)

    return string


if __name__ == '__main__':
    ids  = ['86753879', '86745912', '297066030']
    r = (scrap_profile_info('86745912'))
    print(r)
