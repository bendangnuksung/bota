from bota.utility import heroes
from bota.web_scrap.heroes_process import find_hero_name

class Dotavoyance():
    def __init__(self):
        self.heroes = heroes.heroes_dict()

    def find_by_name(self, hero_name):
        return [x for x in self.heroes["heroes"] if x["name"] == hero_name]

    def find_by_id(self, hero_id):
        return [x for x in self.heroes["heroes"] if x["id"] == hero_id]
    
    def find_by_displayname(self, hero_name):
        return [x for x in self.heroes["heroes"] if x["displayname"] == hero_name]

    def find_by_showname(self, hero_name):
        return [x for x in self.heroes["heroes"] if x["showname"] == hero_name]

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

        return True, hero_names

