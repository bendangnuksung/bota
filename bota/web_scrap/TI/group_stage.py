from bs4 import BeautifulSoup as bs
import requests
from bota.web_scrap.scrap_constant import browser_headers
from bota.utility.discord_display import cvt_dict_to_discord_pretty_text
import re


GROUP_STAGE_URL = 'https://liquipedia.net/dota2/The_International/2019'
GROUPS = ['GROUP A', 'GROUP B']
COLUMNS = ['team_name', 'w-d-l', 'points']


def get_group_stage_table():
    r = requests.get(url=GROUP_STAGE_URL, headers=browser_headers)
    r = r.text
    soup = bs(r, 'html.parser')
    group_tables = soup.find_all('table', {'class': 'table table-bordered grouptable'})

    prepared_group_tables = {}
    for i, group_table in enumerate(group_tables):
        temp_rows = group_table.find_all('tr')
        highest_num = 0
        for temp_row in temp_rows:
            if 'data-toggle-area-content' in temp_row.attrs:
                if int(temp_row.attrs['data-toggle-area-content']) > highest_num:
                    highest_num = int(temp_row.attrs['data-toggle-area-content'])
        highest_num = str(highest_num)
        rows = group_table.find_all('tr', {'data-toggle-area-content': highest_num})
        prepared_row = []
        for row in rows:
            columns = row.find_all('td')
            prepared_cols = {}
            for j, column in enumerate(columns):
                if j == 0:
                    row_contents = column.contents[0]
                    team_name = row_contents.attrs['data-highlightingclass']
                    prepared_cols[COLUMNS[j]] = team_name
                else:
                    prepared_cols[COLUMNS[j]] = column.contents[0].string
            prepared_row.append(prepared_cols)
        prepared_group_tables[GROUPS[i]] = prepared_row
    return prepared_group_tables


def get_group_stage():
    prepared_group_tables = get_group_stage_table()
    pretty_groups = {}
    for table_name, table_value in prepared_group_tables.items():
        pretty_text = cvt_dict_to_discord_pretty_text(table_value, spaces=20, custom_space={'w-d-l': 10, 'points': 5})
        pretty_groups[table_name] = pretty_text

    # adding colour to text with ```diff```
    final_string = ''
    for table_name, string_value in pretty_groups.items():
        split_value = string_value.splitlines()
        string_list = []
        for i, line in enumerate(split_value):
            if i == 0:
                string_to_add = '  ' + line
            elif i < 5:
                string_to_add = '+ ' + line
            else:
                string_to_add = '- ' + line
            # if i == len(split_value) - 1:
            #     string_to_add += 'Eliminate'
            string_list.append(string_to_add)

        join_string = "\n".join(string_list)
        final_string += '**'+table_name+'**```diff\n' + join_string+'```'

    return final_string


def clean_score_result(content):
    score = None
    try:
        score = content.string
        score = re.sub('[^0-9]', '', score)
    except Exception:
        try:
            score = content
            score = re.sub('[^0-9]', '', score)
        except Exception:
            pass
    return score


def get_main_stage_table():
    r = requests.get(url='https://liquipedia.net/dota2/The_International/2019', headers=browser_headers)
    r = r.text
    soup = bs(r, 'html.parser')
    main_stage_table = soup.find('table', {'class': 'table table-striped sortable match-card'})

    prepared_main_tables = []
    for i, main_table in enumerate(main_stage_table.contents[0].contents):
        if i == 0:
            continue
        date = main_table.find('td', {'class': 'Date'}).contents[0].string
        date = date.split(':')[:-1]
        date = ':'.join(date)
        date, time = date.split()
        date = 'AUG ' + date.split('-')[-1]
        date = date + ' ' + time

        round = main_table.find('td', {'class': 'Round'}).string
        round = round.replace('Bracket', '')
        round = round.replace('  ', ' ')
        round = round.replace('s', '')

        score = 'TBD'
        try:
            score_temp = main_table.find('td', {'class': 'Score'})
            team_1_score = score_temp.contents[0]
            team_1_score = clean_score_result(team_1_score)

            team_2_score = score_temp.contents[1]
            team_2_score = clean_score_result(team_2_score)

            if team_1_score is not None and team_2_score is not None:
                score = team_1_score + ':' + team_2_score

        except Exception:
            pass

        try:
            team1 = main_table.find('td', {'class': 'TeamLeft'}).find('a').string
        except Exception:
            team1 = main_table.find('td', {'class': 'TeamLeft'}).find('abbr').string
        try:
            team2 = main_table.find('td', {'class': 'TeamRight'}).find_all('a')[1].string
        except Exception:
            team2 = main_table.find('td', {'class': 'TeamRight'}).find('abbr').string

        prepared_main_tables.append({'date: utc': date, 'round': round, 'team 1': team1, 'score': score, 'team 2': team2})

    return prepared_main_tables


def get_main_stage():
    main_stage_table = get_main_stage_table()
    time_zone_string = 'Check your Local timing from [here](https://www.timeanddate.com/time/current-number-time-zones.html) \n'
    main_stage_table = cvt_dict_to_discord_pretty_text(main_stage_table, show_index=False,
                                                       custom_space={'date: utc': 13, 'round': 12, 'score': 6, 'team 1': 8, 'team 2': 8})
    main_stage_table = f'{time_zone_string}```cs\n{main_stage_table}```'
    return main_stage_table


if __name__ == '__main__':
    string = get_main_stage()
    # string = get_group_stage()
    print(string)
