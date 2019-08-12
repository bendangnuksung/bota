from bota.utility import heroes
from bota.web_scrap.heroes_process import find_hero_name
from bota import constant
import bota.web_scrap.heroes_process as bota_hp
import bota.image_processing as bota_imp

import numpy as np
import cv2
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
        num_heroes = 0

        hero_names = []
        send_names = []
        for hn in hero_strings:
            found_hero, fullname = find_hero_name(hn)
            if found_hero:
                hero_names.append(fullname)
                send_names.append(fullname)
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

        req_str = "https://www.dotavoyance.com/explore?heroes[]="+",".join(hero_ids)+"&results_offset=0&sort_column=perc_win_total&sort_direction=-1&column_filters=%7B%22total_matches%22:%7B%22upper%22:0,%22lower%22:50%7D%7D&table_to_use=7.21"
        r = requests.get(req_str,  headers={'user-agent': 'Mozilla/5.0'})
        results = r.json()

        if len(hero_strings) != num_heroes:
            return False, ''

        img_good, dv_img_path = self.make_counters_image(results, num_heroes)

        return img_good, dv_img_path

    def make_counters_image(self, response_json, num_heroes):
        if response_json['versus_results'] == []:
            return False, ''

        img_height, img_width = constant.DV_DEFAULT_IMAGE_HEIGHT, constant.DV_DEFAULT_IMAGE_WIDTH
        n_channels = constant.DV_NUM_CHANNELS
        transparent_img = np.zeros((img_height, img_width, n_channels), dtype=np.uint8)
        cv2.imwrite('bota/data/background/transparent.png', transparent_img)

        img0 = cv2.imread('bota/data/background/transparent.png')
        icon_dims = cv2.imread('bota/data/character_icons_big/axe.png').shape
        img0, header_height = self.write_counter_header(img0, num_heroes, icon_dims)
        res_count = 0
        curr_height = constant.DV_HEIGHT_BUFFER + header_height

        for res in response_json['versus_results']:
            max_img_h = 0
            img_save_name = res['heroes_index']
            res_count = res_count + 1
            if res_count > 9:
                break

            
            the_side = 'a'
            if res['heroes_index'] == res['heroes_a_index']:
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
                    img = cv2.imread('bota/data/character_icons_big/'+bota_name+'.png')
                    img_h = img.shape[0]
                    img_w = img.shape[1]
                    img0[curr_height: img_h + curr_height, curr_width: img_w + curr_width, :] = img
                    curr_width = curr_width + img_w
                    max_img_h = max([img_h, max_img_h])
                
            img0 = self.write_counter_row(img0, 0, res_count, icon_dims, res, num_heroes)
            curr_height = curr_height + max_img_h + constant.DV_HEIGHT_BUFFER
            

        dv_img_path = '/tmp/counter_' + img_save_name + '.png'
        cv2.imwrite(dv_img_path, img0)

        return True, dv_img_path

    def write_counter_header(self, the_image, num_heroes, icon_dims):
        img_h = icon_dims[0]
        img_w = icon_dims[1]
        text_pos = (num_heroes*img_w + constant.DV_COLUMN_BUFFER, img_h/2)
        the_text = "Win %"
        the_image = bota_imp.write_text_pil(the_image, the_text, text_pos, size=constant.PLAYER_NAME_FONT_SIZE)       

        return the_image, img_h

    def write_counter_row(self, the_image, col_index, row_index, icon_dims, result_json, num_heroes):
        img_h = icon_dims[0]
        img_w = icon_dims[1]
        text_pos = ((num_heroes + col_index)*img_w + constant.DV_COLUMN_BUFFER, img_h/4 + (img_h+constant.DV_HEIGHT_BUFFER)*row_index)
        the_text = str(round((1.0-result_json['perc_win_total'])*100))
        the_image = bota_imp.write_text_pil(the_image, the_text, text_pos, size=constant.PLAYER_NAME_FONT_SIZE)       

        return the_image

    def get_hero_name_from_id(self, hero_id):

        return hero_name


