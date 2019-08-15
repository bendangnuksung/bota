from bs4 import BeautifulSoup as bs
import requests
from bota.web_scrap.scrap_constant import browser_headers
from bota.utility.discord_display import cvt_dict_to_discord_pretty_text


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
        rows = group_table.find_all('tr', {'data-toggle-area-content': '1'})
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
        pretty_text = cvt_dict_to_discord_pretty_text(table_value, spaces=20, custom_space={'w-l-d': 10, 'points': 5})
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


if __name__ == '__main__':
    string = get_group_stage()
    print(string)
