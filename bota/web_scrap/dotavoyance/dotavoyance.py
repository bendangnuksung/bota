from bota.web_scrap.dotavoyance import heroes
from bota.web_scrap.heroes_process import find_hero_name
from bota import constant
import bota.web_scrap.heroes_process as bota_hp
import bota.image_processing as bota_imp
from bota.constant import REPO_PATH
import os

import numpy as np
import cv2
import requests

class Dotavoyance():
    def __init__(self):
        self.heroes = heroes.heroes_dict()

    def find_by_name(self, hero_name):
        return [x for x in self.heroes["heroes"] if x["name"] == hero_name.lower()]

    def find_by_id(self, hero_id):
        hero_id = int(hero_id)
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

    def parse_heroes(self, message_string):
        message_string, sep, skill = message_string.partition('-')
        message_string = message_string.split()
        message_string = ' '.join(message_string[1:])
        message_string = message_string.strip()
        hero_strings = message_string.split(",")
        return hero_strings, skill

    def get_sort_col(self, skill):
        col_skill = {
                'high': 'perc_win_top',
                'med': 'perc_win_middle',
                'low': 'perc_win_bottom',
                '': 'perc_win_total'
                }
        return col_skill[skill]

    def get_hero_ids(self, hero_strings):
        num_heroes = 0

        hero_names = []
        for hn in hero_strings:
            found_hero, fullname = find_hero_name(hn)
            if found_hero:
                hero_names.append(fullname)
            else:
                hero_names.append(hn)

        hero_ids = []
        for hn in hero_names:
            hi = self.find_hero_info(hn)
            if len(hi) > 0:
                dv_hero_info = self.find_hero_info(hn)[0]
                if dv_hero_info != []:
                    hero_ids.append(str(dv_hero_info["id"]))
                    num_heroes = num_heroes + 1

        return hero_ids, num_heroes

    def get_meta(self, message_string):
        num_heroes, skill = self.parse_heroes(message_string)
        num_heroes = num_heroes[0]
        sort_col = self.get_sort_col(skill)

        req_str = "https://www.dotavoyance.com/overall"
        r = requests.get(req_str,  headers={'user-agent': 'Mozilla/5.0'})
        results = r.json()

        week_results = results['last_week']
        num_week_results = [d for d in week_results if int(d['num_heroes']) == int(num_heroes)]

        return_results = []
        for the_summary in num_week_results:
            st = the_summary['summary_type']
            this_result = {}
            the_heroes = []
            if "counter" not in st:
                hero_ids = the_summary['heroes_index'].split("_")
                for h_id in hero_ids:
                    curr_name = self.find_by_id(h_id)[0]['displayname']
                    name_found, bota_name = bota_hp.find_hero_name(curr_name)
                    if name_found:
                        the_heroes.append(bota_name)
                the_summary['heroes'] = the_heroes
                return_results.append(the_summary)

        return True, return_results


    ## Combos
    def get_combos(self, message_string):
        num_heroes, skill = self.parse_heroes(message_string)
        num_heroes = num_heroes[0]
        sort_col = self.get_sort_col(skill)

        minimum_num_games = 25
        if num_heroes > 2:
            minimum_num_games = 5

        req_str = "https://www.dotavoyance.com/combos?numHeroes="+num_heroes+"&results_offset=0&sort_column="+sort_col+"&sort_direction=1&column_filters=%7B%22total_matches%22:%7B%22upper%22:0,%22lower%22:"+str(minimum_num_games)+"%7D%7D&table_to_use=Last Week"
        r = requests.get(req_str,  headers={'user-agent': 'Mozilla/5.0'})
        results = r.json()

        res_count = 0
        hero_results = []
        for res in results:
            this_result = {}
            res_count = res_count + 1
            if res_count > 9:
                break

            hero_titles =[
                    'hero_one',
                    'hero_two',
                    'hero_three',
                    'hero_four',
                    'hero_five',
                    ]

            res_hero_names = []
            curr_width = 0
            for nh in range(int(num_heroes)):
                h_id = res[hero_titles[nh]]
                curr_name = self.find_by_id(h_id)[0]['displayname']
                name_found, bota_name = bota_hp.find_hero_name(curr_name)
                if name_found:
                    res_hero_names.append(bota_name)
            
            this_result['win_percentage'] = round((res[sort_col])*100)
            this_result['heroes'] = res_hero_names
            hero_results.append(this_result)

        return True, hero_results


    ## Teammates
    def get_teammates(self, message_string):
        hero_strings, skill = self.parse_heroes(message_string)
        sort_col = self.get_sort_col(skill)
        hero_ids, num_heroes = self.get_hero_ids(hero_strings)

        minimum_num_games = 50
        if num_heroes > 2:
            minimum_num_games = 5

        req_str = "https://www.dotavoyance.com/teammates?heroes[]="+",".join(hero_ids)+"&results_offset=0&sort_column="+sort_col+"&sort_direction=1&column_filters=%7B%22total_matches%22:%7B%22upper%22:0,%22lower%22:"+str(minimum_num_games)+"%7D%7D&table_to_use=Last Week"
        r = requests.get(req_str,  headers={'user-agent': 'Mozilla/5.0'})
        results = r.json()

        if len(hero_strings) != num_heroes:
            return False, ''

        res_count = 0
        hero_data = []
        for res in results:
            the_heroes = set(res['heroes_index'].split("_"))
            the_perc = round((res[sort_col])*100)
            tm_heroes = list(the_heroes - set(hero_ids))
            if len(tm_heroes) > 1:
                print("Should not be more than 1")
            hero_info = self.find_by_id(tm_heroes[0])[0]
            hero_info['win_percentage'] = the_perc
            hero_data.append(hero_info)
            res_count = res_count + 1
            if res_count > 9:
                break

        img_good, hero_results = self.make_teammates_results(hero_data)

        return img_good, hero_results

    def make_teammates_results(self, hero_data):
        if len(hero_data) < 2:
            return False, ''

        res_count = 0
        hero_results = []
        for hd in hero_data:
            this_result = {}
            res_count = res_count + 1
            
            res_hero_names = []
            curr_width = 0
            curr_name = hd['displayname']
            name_found, bota_name = bota_hp.find_hero_name(curr_name)
            if name_found:
                res_hero_names.append(bota_name)
            
            this_result['win_percentage'] = hd['win_percentage']
            this_result['heroes'] = res_hero_names
            hero_results.append(this_result)
            
        return True, hero_results

    ## Counters
    def get_counters(self, message_string):
        hero_strings, skill = self.parse_heroes(message_string)
        sort_col = self.get_sort_col(skill)
        hero_ids, num_heroes = self.get_hero_ids(hero_strings)

        minimum_num_games = 50
        if num_heroes > 2:
            minimum_num_games = 5

        req_str = "https://www.dotavoyance.com/explore?heroes[]="+",".join(hero_ids)+"&results_offset=0&sort_column="+sort_col+"&sort_direction=-1&column_filters=%7B%22total_matches%22:%7B%22upper%22:0,%22lower%22:"+str(minimum_num_games)+"%7D%7D&table_to_use=Last Week"
        r = requests.get(req_str,  headers={'user-agent': 'Mozilla/5.0'})
        results = r.json()

        if len(hero_strings) != num_heroes:
            return False, ''

        img_good, hero_results = self.make_counters_results(results, num_heroes, hero_ids, sort_col)

        return img_good, hero_results

    
    def make_counters_results(self, response_json, num_heroes, curr_hero_ids, sort_col):
        if response_json['versus_results'] == []:
            return False, ''

        res_count = 0
        hero_results = []

        for res in response_json['versus_results']:
            this_result = {}
            max_img_h = 0
            img_save_name = res['heroes_index']
            res_count = res_count + 1
            if res_count > 9:
                break

            
            the_side = 'a'
            if str(res['hero_a_one']) in curr_hero_ids:
                the_side = 'b'

            hero_titles =[
                    'hero_' + the_side + '_one',
                    'hero_' + the_side + '_two',
                    'hero_' + the_side + '_three',
                    'hero_' + the_side + '_four',
                    'hero_' + the_side + '_five',
                    ]

            res_hero_names = []
            curr_width = 0
            for nh in range(num_heroes):
                h_id = res[hero_titles[nh]]
                curr_name = self.find_by_id(h_id)[0]['displayname']
                name_found, bota_name = bota_hp.find_hero_name(curr_name)
                if name_found:
                    res_hero_names.append(bota_name)
            
            this_result['win_percentage'] = round((1.0-res[sort_col])*100)
            this_result['heroes'] = res_hero_names
            hero_results.append(this_result)

        return True, hero_results


