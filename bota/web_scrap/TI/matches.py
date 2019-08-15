from bs4 import BeautifulSoup as bs
import requests
from bota.web_scrap.scrap_constant import browser_headers
from bota.utility.discord_display import cvt_dict_to_discord_pretty_text


GROUP_STAGE_MATCHES = 'https://www.dotabuff.com/esports/leagues/10749-the-international-2019/schedule'


def get_upcoming_matches():
    upcoming_matches = []
    r = requests.get(url=GROUP_STAGE_MATCHES, headers=browser_headers)
    r = r.text
    soup = bs(r, 'html.parser')
    match_contents = soup.find_all('div', {'class':'content-inner'})
    group_stage_day_matches = None
    flag = False
    for content in match_contents:
        headers = content.find_all('header')
        for header in headers:
            if header is not None:
                if header.string == 'Schedule':
                    flag = True
                    group_stage_day_matches = content.find('tbody')
                    break

    if not flag:
        return upcoming_matches

    for i, row in enumerate(group_stage_day_matches.contents):
        if i % 3 != 0:
            continue

        anchor = row.find('a')
        series = anchor.string
        bracket = row.contents[1].contents[0].string
        time_str = str(row.contents[2].find('time').string)
        date, time_others = time_str.split(',')
        time = time_others.split()[1:]
        time = date + ", " + " ".join(time)

        team_1 = row.contents[4].find('div', {'class': 'team team-1'})
        team_1 = team_1.contents[1].contents[0].contents[0].string
        team_2 = row.contents[4].find('div', {'class': 'team team-2'})
        team_2 = team_2.contents[1].contents[0].contents[0].string

        upcoming_matches.append({'series': series, 'bracket': bracket, 'team 1': team_1, 'team 2': team_2,
                                 'time': time})
        # print(i,series, bracket, time, team_1, team_2)
    return upcoming_matches


def get_all_matches():
    header = '**Upcoming TI Matches**. Check your local timing from :\n' \
             '<https://www.timeanddate.com/time/current-number-time-zones.html>\n'
    upcoming_matches = get_upcoming_matches()
    upcoming_matches = cvt_dict_to_discord_pretty_text(upcoming_matches,
                                                       custom_space={'series': 7, 'bracket': 9, 'team 1': 18,
                                                                     'team 2': 18, 'time':18})

    final_string = f'{header}```cs\n{upcoming_matches}```'
    return final_string


if __name__ == '__main__':
    print(get_all_matches())
