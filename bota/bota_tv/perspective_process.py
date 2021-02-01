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

    def __init__(self, update_after=100000): # update after every 5 hours
        self.first_update = False
        self.update_after = update_after

    def _init_heros(self):
        self.hero_perspective_info = {}
        self.all_video_info = []
        for heroname in heroes_names:
            heroname = d2pt_hero_names[heroname]
            self.hero_perspective_info[heroname] = []

    def extract_info(self, description):
        description = description.lower()
        description_lines = description.split("\n")
        heroname = None
        playername = None
        position = None
        mmr = None
        for line in description_lines:
            if line.startswith("hero"):
                heroname = line.split(":")[1]

            elif line.startswith("player"):
                playername = line.split(":")[1:]
                playername = ":".join(playername)

            elif line.startswith("mmr"):
                mmr = line.split(":")[1]

            elif line.startswith("position"):
                position = line.split(":")[1]

        return heroname, playername, position, mmr

    def load_last_saved_link(self, last_saved_pth):
        f = open(last_saved_pth)
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

    def _update_vids(self, r=None, force_update=False, last_saved_pth=constant.YT_LINK_PATH):
        if not force_update:
            if os.path.exists(last_saved_pth):
                file_old = is_file_old(last_saved_pth, self.update_after)
                if not file_old:
                    print("Loading from saved YT links (file not old)")
                    self.load_last_saved_link(last_saved_pth)
                    return
                else:
                    print("File outdated, updating to latest ")

        if r is None:
            try:
                all_vid_info = ytvideo.get_video_links()
                self.update_hero_win_rate()
            except Exception as e:
                print("Failed to update: ", e)
                if os.path.exists(last_saved_pth):
                    self.load_last_saved_link(last_saved_pth)
                return
        else:
            all_vid_info = r
        self._init_heros()
        videos_info = []
        for vid_info in all_vid_info:
            heroname, playername, position, mmr = self.extract_info(vid_info['description'])
            if heroname is None:
                print("No hero name")
            heroname = camel_case(heroname)
            link = vid_info['link']
            published = vid_info['published']
            infos = {'heroname': heroname, 'player': playername,'mmr': mmr, 'link': link, 'published': published, 'position': position}
            videos_info.append(infos)

        self.all_video_info = sorted(videos_info, key=itemgetter('published'), reverse=True)

        for info in self.all_video_info:
            heroname = info['heroname']
            self.hero_perspective_info[heroname].append(info)

        with open(last_saved_pth, 'w') as fp:
            json.dump(self.hero_perspective_info, fp, indent=4, default=str)

        with open(constant.ALL_YT_LINK_PATH, 'w') as fp:
            json.dump(self.all_video_info, fp, indent=4, default=str)

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
        if 'update' in argument.lower() and is_admin:
            print("Force update")
            self._update_vids(force_update=True)
            embed = discord.Embed(description='Update Youtube links Successfull', color=discord.Color.green())
            return True, '', embed

        if not self.first_update: # update only during the first call
            self._update_vids()
            self.update_hero_win_rate()
            self.last_update = datetime.now()
            self.first_update = True
        else:
            current_time = datetime.now()
            time_diff = (current_time - self.last_update).total_seconds()
            if time_diff >= self.update_after:
                self._update_vids()
                self.last_update = datetime.now()

        heroname = argument
        if len(heroname) < 1:
            text = self.pretty_text_latest_vid()
            embed = self.embed_message('latest', text)
            return True, heroname, embed

        flag, heroname = find_hero_name(heroname)
        flag = False if heroname == '' else True
        if not flag:
            return False, heroname, ''

        heroname = d2pt_hero_names[heroname]
        text = self.pretty_text_for_hero(heroname)
        embed = self.embed_message(heroname, text)
        return True, heroname, embed


if __name__ == '__main__':
    # print(camel_case("queen of pain"))
    pp = PlayersPerspective()
    flag, result, embed = pp.get_perspective('od')
    print(flag, embed.description)
    # t = pp.get_perspective("")
    # print(t)
