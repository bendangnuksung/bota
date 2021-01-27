from bs4 import BeautifulSoup as bs
import requests
from bota.web_scrap.scrap_constant import browser_headers
from bota.web_scrap.scrap import find_hero_name
from bota import constant
from datetime import datetime
import discord


url = 'https://dota2.gamepedia.com/Aghanim%27s_Scepter/Upgraded_Abilities'


class Agha():
    def __init__(self, update_n_sec=86400, url=url):
        self.url = url
        self.update_after = update_n_sec
        self.agha_info = {}

    def _update_info(self):
        url = self.url
        r = requests.get(url=url, headers=browser_headers)
        r = r.text
        soup = bs(r, 'html.parser')
        agha_info = soup.find_all('li', {'class': 'skilllist-rich'})
        self.agha_info = {}
        for i, info in enumerate(agha_info):
            try:
                a = info.find_all('a')
                name = a[0].string

                flag, hero_name = find_hero_name(name)
                if not flag:
                    continue

                skill_name = a[1].string
                try:
                    skill_image_url = info.find('img').attrs['src']
                except Exception:
                    skill_image_url = ''
                temp_desc = info.find_all('b')
                key_desc = {}
                for desc in temp_desc:
                    key_desc[desc.string] = desc.next_sibling
                summary = info.find('i').string
                if summary is None:
                    summary = f'\nSource: **[dota2.gamepedia.com]({self.url})**'
                else:
                    summary += f'\nSource: **[dota2.gamepedia.com]({self.url})**'
                self.agha_info[hero_name] = {'skill_name': skill_name, 'skill_image_url': skill_image_url,
                                             'key_desc': key_desc, 'summary': summary}
            except Exception as e:
                print(e)
                continue
        self.last_update = datetime.now()

    def embed_message(self, hero_name, info):
        if info is not None:
            title = f"{hero_name.upper()} : {info['skill_name']}"
            description = f'Aghanim Scepter upgrade for **{hero_name.upper()}**'
            embed = discord.Embed(description=description, color=discord.Color.blurple())
        else:
            title = f"{hero_name.upper()}"
            description = f'No Aghanim Scepter for **{hero_name.upper()}**'
            embed = discord.Embed(description=description, color=discord.Color.red())

        embed.set_author(name=title,
                         icon_url=f'{constant.CHARACTER_ICONS_URL}{hero_name}.png',
                         url=self.url)
        if info is not None:
            for key, value in info['key_desc'].items():
                embed.add_field(name=key.upper(), value=value)
            embed.add_field(name='Summary', value=info['summary'])
        # image_file = discord.File(image_path, os.path.basename(image_path))
            embed.set_thumbnail(url=info['skill_image_url'])
        return embed

    def get_agha_info(self, hero_name):
        current_time = datetime.now()
        if (self.agha_info == {}) or ((current_time - self.last_update).total_seconds() > self.update_after):
            self._update_info()

        flag, hero_name = find_hero_name(hero_name)
        flag = False if hero_name == '' else True
        if not flag:
            return False, hero_name, ''
        # if hero_name not in self.agha_info:
        #     return False, ''
        info = self.agha_info.get(hero_name)
        embed_msg = self.embed_message(hero_name, info)
        return True, hero_name, embed_msg


if __name__ == '__main__':
    a = Agha()
    print(a.get_agha_info('snap'))
