from bs4 import BeautifulSoup as bs
import requests
from bota.web_scrap.scrap_constant import browser_headers
from bota.utility.discord_display import cvt_dict_to_discord_pretty_text


MOST_HEROES_PLAYED_URL = 'https://www.dotabuff.com/esports/leagues/10749-the-international-2019/heroes'
PICK_BANS_URL = 'https://www.dotabuff.com/esports/leagues/10749-the-international-2019/picks'


def scrap_most_played_heroes(top=10):
    r = requests.get(url=MOST_HEROES_PLAYED_URL, headers=browser_headers)
    r = r.text
    soup = bs(r, 'html.parser')
    hero_list = soup.find('tbody')
    most_played_heroes = []
    for i, row in enumerate(hero_list.contents, 1):
        if i > top:
            break
        # temp = {}
        hero_name = row.find('img', {'class': 'img-hero img-icon'})
        hero_name = hero_name.attrs['alt']

        others = row.find_all('td', {'class': ['r-tab', 'r-group-1']})

        total_matches = others[0].attrs['data-value']
        win_rate = others[1].attrs['data-value'] + '%'
        win_rate = win_rate.replace('%', '')
        integers, floats = win_rate.split('.')
        win_rate = integers + '.' + floats[:2] + '%'

        kda = others[2].attrs['data-value']
        kda = "%.2f" % (float(kda))

        most_played_heroes.append({'hero': hero_name, 'matches': total_matches, 'win rate': win_rate, 'kda': kda})
    return most_played_heroes


def get_high_kda_heroes(top=10):
    r = requests.get(url=MOST_HEROES_PLAYED_URL, headers=browser_headers)
    r = r.text
    soup = bs(r, 'html.parser')
    kda_heroes = soup.find('table', {'class': 'table sortable table-striped table-condensed'}).contents[1]
    high_kda_heroes = []
    for i, row in enumerate(kda_heroes.contents, 1):
        if i > top:
            break
        others = row.find_all('td')

        hero_name = others[1].contents[0].string
        kda = others[2].attrs['data-value']
        kda = "%.2f" % float(kda)

        high_kda_heroes.append({'hero': hero_name, 'kda': kda})
    return high_kda_heroes


def get_pick_ban_heroes(top=10):
    r = requests.get(url=PICK_BANS_URL, headers=browser_headers)
    r = r.text
    soup = bs(r, 'html.parser')
    pick_bans_table = soup.find('tbody')
    pick_ban = []
    for i, row in enumerate(pick_bans_table.contents, 1):
        if i > top:
            break
        others = row.find_all('td')

        hero_name = others[1].contents[1].string

        pick = others[2].contents[0].string
        pick_win_rate = others[3].contents[0].string

        ban = others[4].contents[0].string
        ban_win_rate = others[5].contents[0].string

        pick_ban.append({'hero': hero_name, 'pick': pick, 'pick win rate': pick_win_rate, 'ban': ban, 'ban_win_rate': ban_win_rate})
    return pick_ban


def get_all_stats():
    pick_ban_stats = get_pick_ban_heroes(top=5)
    pick_ban_stats = cvt_dict_to_discord_pretty_text(pick_ban_stats, rename_keys={'pick win rate': 'p-win', 'ban_win_rate': 'b-win'},
                                                     custom_space={'pick': 5, 'p-win':8, 'ban': 5, 'b-win': 7})
    pick_ban_stats_string = f'**Pick/Ban Stats** ```cs\n{pick_ban_stats}```'

    most_played_hero = scrap_most_played_heroes(top=5)
    most_played_hero = cvt_dict_to_discord_pretty_text(most_played_hero, rename_keys={'matches': 'match', 'win rate': 'win %'},
                                                       custom_space={'match': 7, 'win %': 8, 'kda': 5})
    most_played_hero_string = f"**Most Played Heroes** ```cs\n{most_played_hero}```"

    highest_kda_hero = get_high_kda_heroes(top=5)
    highest_kda_hero = cvt_dict_to_discord_pretty_text(highest_kda_hero)
    highest_kda_hero_string = f"**Highest KDA Heroes** ```cs\n{highest_kda_hero}```"

    head = "**TI9 Stats** including TI qualifiers match \n"
    final_string = head + pick_ban_stats_string + most_played_hero_string + highest_kda_hero_string

    return final_string


if __name__ == '__main__':
    r = get_all_stats()
    print(r)
    exit()
    pick_ban = get_pick_ban_heroes()
    pick_ban = cvt_dict_to_discord_pretty_text(pick_ban)
    print(pick_ban)
    kda = get_high_kda_heroes()
    kda = cvt_dict_to_discord_pretty_text(kda)
    print(kda)
    most_played = scrap_most_played_heroes()
    most_played = cvt_dict_to_discord_pretty_text(most_played)
    print(most_played)
