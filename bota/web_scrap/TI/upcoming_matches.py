from bs4 import BeautifulSoup as bs
import requests
from bota.web_scrap.scrap_constant import browser_headers
from bota.utility.discord_display import cvt_dict_to_discord_pretty_text


GROUP_STAGE_MATCHES = 'https://liquipedia.net/dota2/The_International/2018/Group_Stage'


def liquid_upcoming_matches():
    r = requests.get(url=GROUP_STAGE_MATCHES, headers=browser_headers)
    r = r.text
    soup = bs(r, 'html.parser')
    group_stage_day_matches = soup.find('div', {'class': 'toggle-group toggle-state-hide'})
    for i, day in enumerate(group_stage_day_matches.contents):
        print(day)


if __name__ == '__main__':
    liquid_upcoming_matches()
