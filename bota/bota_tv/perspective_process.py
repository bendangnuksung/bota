# from bota.bota_tv.youtube_process import YoutubeVideo
from bota.bota_tv.youtube_dl_process import YoutubeVideo
from bota.web_scrap.scrap_constant import heroes_names, d2pt_hero_names
from datetime import datetime
from bota.web_scrap.scrap import find_hero_name
import discord
from bota import constant
from bota.utility.general import is_file_old
import os
import json
from operator import itemgetter
from bs4 import BeautifulSoup as bs
import requests


ytvideo = YoutubeVideo()

stop_words = ['of', 'the']


def camel_case(txt):
    final_txt = []
    for word in txt.split():
        word = word[0].upper() + word[1:].lower()
        if "-" in word:
            words = word.split("-")
            word = words[0] + '-' + words[1][0].upper() + words[1][1:].lower()

        if word.lower() in stop_words:
            word = word.lower()
        final_txt.append(word)

    return " ".join(final_txt)


class PlayersPerspective:

    def __init__(self, update_after=7200): # update after every 5 hours
        self.first_update = False
        self.update_after = update_after
        self.update_hero_win_rate()
        self.load_last_saved_link()

    def _init_heros(self):
        self.hero_perspective_info = {}
        self.all_video_info = []
        for heroname in heroes_names:
            heroname = d2pt_hero_names[heroname]
            self.hero_perspective_info[heroname] = []

    def load_last_saved_link(self):
        f = open(constant.YT_LINK_PATH)
        self.hero_perspective_info = json.load(f)

        f = open(constant.ALL_YT_LINK_PATH)
        self.all_video_info = json.load(f)

    def update_hero_win_rate(self, url="https://www.dotabuff.com/heroes/winning?date=week"):
        self.heroes_win_rate = {}
        r = requests.get(url, headers={'user-agent': 'google bot'})
        bs_soup = bs(r.text, "html.parser")
        soup = bs_soup.find('tbody')
        rows = soup.findAll('tr')
        for row in rows:
            tds = row.findAll('td')

            heroname = tds[0].attrs['data-value']
            flag, dotabuff_hero_name = find_hero_name(heroname)
            winrate = str(round(float(tds[2].attrs['data-value']), 2))
            pickrate = str(round(float(tds[3].attrs['data-value']), 2))
            kda = str(round(float(tds[4].attrs['data-value']), 2))
            self.heroes_win_rate[dotabuff_hero_name] = {'winrate': winrate, 'pickrate': pickrate, 'kda': kda}

    def pretty_text_for_hero(self, heroname, max_row=12):
        # final_string = f"```diff\n-{heroname} Perspective: ```\n"
        final_string = ""
        for i, data in enumerate(self.hero_perspective_info[heroname], 1):
            if i >= max_row:
                break
            try:
                published_data = datetime.fromisoformat(data["published"])
            except:
                published_data = data['published']
            now = datetime.now()
            days_ago = (now - published_data).days

            if days_ago < 31:
                final_ago = days_ago
                day_string = "days" if final_ago > 1 else "day"
            else:
                final_ago = days_ago // 31
                day_string = "month" if final_ago < 2 else "months"

            data["player"] = "Unknown" if data["player"] == "None" else data["player"]
            data["position"] = "Unknown" if data["position"] == "none" else data["position"]

            final_string += f'{i}. **{data["player"]}**' \
                            f'  `Pos:` {data["position"]}' \
                            f'  `MMR:` {data["mmr"]} ' \
                            f'  `{final_ago} {day_string} ago`' \
                            f'   __**[LINK]({data["link"]})**__\n\n'

        return final_string

    def pretty_text_latest_vid(self, max_row=15):
        final_string = ""
        for i, data in enumerate(self.all_video_info, 1):
            if i >= max_row:
                break
            # title =
            try:
                published_data = datetime.fromisoformat(data["published"])
            except:
                published_data = data['published']
            now = datetime.now()
            days_ago = (now - published_data).days

            if days_ago < 31:
                final_ago = days_ago
                day_string = "days" if final_ago > 1 else "day"
            else:
                final_ago = days_ago // 31
                day_string = "month" if final_ago < 2 else "months"

            data["player"] = "Unknown" if data["player"] == "None" else data["player"]
            data["position"] = "Unknown" if data["position"] == "none" else data["position"]

            final_string += f'{i}. **{data["heroname"]}** _By_' \
                            f'  __**{data["player"]}**__ ' \
                            f'  `Pos:` {data["position"]}' \
                            f'  `MMR:` {data["mmr"]} ' \
                            f'  `{final_ago} {day_string} ago`' \
                            f'   __**[LINK]({data["link"]})**__\n\n'
        return final_string

    def embed_message(self, hero_name, text):
        flag, dotabuff_hero_name = find_hero_name(hero_name)
        if hero_name != 'latest':
            title = f"{hero_name.upper()} Perspective \nLast WeekStats: Win: {self.heroes_win_rate[dotabuff_hero_name]['winrate']}% | Pick: {self.heroes_win_rate[dotabuff_hero_name]['pickrate']}% | KDA: {self.heroes_win_rate[dotabuff_hero_name]['kda']}"
            description = f'{hero_name} Perspective Youtube videos in 1440p'
            thumbnail_path = f'{constant.CHARACTER_ICONS_URL}{dotabuff_hero_name}.png'
        else:
            title = f"Heroes Perspective"
            description = f'Perspective Youtube videos in 1440p'
            thumbnail_path = constant.DOTA2_LOGO_URL

        embed = discord.Embed(description=text, color=discord.Color.from_rgb(175, 232, 109))

        embed.set_author(name=title,
                         icon_url=constant.BOTA_LOGO_URL,
                         url=constant.YOUTUBE_CHANNEL_URL)
        embed.set_thumbnail(url=thumbnail_path)

        return embed

    def get_perspective(self, argument, is_admin=False):
        if os.path.exists(constant.YT_LINK_PATH):
            if is_file_old(constant.YT_LINK_PATH, self.update_after):
                self.update_hero_win_rate()
                self.load_last_saved_link()

        heroname = argument
        # get latest uploaded videos
        if len(heroname) < 1:
            text = self.pretty_text_latest_vid()
            embed = self.embed_message('latest', text)
            return True, heroname, embed

        flag, heroname = find_hero_name(heroname)
        flag = False if heroname == '' else True
        if not flag:
            return False, heroname, ''

        # Get YT videos based on hero
        heroname = d2pt_hero_names[heroname]
        text = self.pretty_text_for_hero(heroname)
        embed = self.embed_message(heroname, text)
        return True, heroname, embed


if __name__ == '__main__':
    pp = PlayersPerspective()
    flag, result, embed = pp.get_perspective('timber')
    print(flag, embed.description)
    # t = pp.get_perspective("")
    # print(t)
