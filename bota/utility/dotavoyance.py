from bota.utility import heroes
from bota.web_scrap.heroes_process import find_hero_name
import requests

class Dotavoyance():
    def __init__(self):
        self.heroes = heroes.heroes_dict()

    def find_by_name(self, hero_name):
        return [x for x in self.heroes["heroes"] if x["name"] == hero_name.lower()]

    def find_by_id(self, hero_id):
        return [x for x in self.heroes["heroes"] if x["id"] == hero_id]
    
    def find_by_displayname(self, hero_name):
        return [x for x in self.heroes["heroes"] if x["displayname"] == hero_name.lower()]

    def find_by_showname(self, hero_name):
        return [x for x in self.heroes["heroes"] if x["showname"].lower() == hero_name.lower()]

    def find_hero_info(self, hero_name):
        hero_info = self.find_by_displayname(hero_name)
        if hero_info == []:
            hero_info = self.find_by_displayname(hero_name.replace("-",""))
            if hero_info == []:
                hero_info = self.find_by_showname(hero_name)
                if hero_info == []:
                    hero_info = self.find_by_showname(hero_name.replace("-",""))

        return hero_info

    def get_counters(self, message_string):
        message_string = message_string.split()
        message_string = ' '.join(message_string[1:])
        message_string = message_string.strip()
        hero_strings = message_string.split(",")

        hero_names = []
        for hn in hero_strings:
            found_hero, fullname = find_hero_name(hn)
            if found_hero:
                hero_names.append(fullname)
            else:
                hero_names.append(hn)

        heroe_ids = []
        for hn in hero_names:
            dv_hero_info = self.find_hero_info(hn)[0]
            if dv_hero_info != []:
                heroe_ids.append(str(dv_hero_info["id"]))

        req_str = "https://www.dotavoyance.com/explore?heroes[]="+",".join(heroe_ids)+"&results_offset=0&sort_column=perc_win_total&sort_direction=1&column_filters=%7B%7D&table_to_use=7.21"
        r = requests.get(req_str,  headers={'user-agent': 'Mozilla/5.0'})
        results = r.json()
        return True, heroe_ids 

