import pandas as pd
import dota2api
from bota.utility import DataFrame_to_image, is_file_old
from bota.constant import GAME_MODE
from bota.web_scrap.scrap_constant import browser_headers_chrome
from bota.private_constant import DOTA2_API_KEY
from bota import constant
from bota.utility import render_mpl_table
import requests
import cv2
import random

dota_api = dota2api.Initialise(DOTA2_API_KEY)


# Dota 2 ProTracker
def get_notable_hero_from_d2pt():
	url = constant.D2PT_URL_LIVE_GAMES
	results = requests.get(url, headers=browser_headers_chrome)
	results = results.json()
	final_result = {}
	for match in results:
		match_id = match[constant.KEYWORD_MATCH_ID]
		notable_player_from_dires = []
		notable_player_from_radiant = []
		for player_details in match['dire']:
			notable_player_from_dires.append(player_details['name'])
		for player_details in match['radiant']:
			notable_player_from_radiant.append(player_details['name'])

		notable_players = notable_player_from_radiant + notable_player_from_dires
		random.shuffle(notable_players)
		notable_players = ",".join(notable_players[:2])
		final_result[match_id] = notable_players
	return final_result


def get_top_games(length=10):
	"""
	Creates a table image of current top live games
	:param length:
	:return: table image path
	"""
	# If TLG image already exist and hasnt been modified in given Threshold second return the same image
	# if not is_file_old(constant.TLG_IMAGE_PATH, constant.TLG_IMAGE_UPDATE_TIME_THRESHOLD):
	# 	return constant.TLG_IMAGE_PATH

	game_list = dota_api.get_top_live_games()
	game_list = game_list['game_list']

	notable_player_dict = get_notable_hero_from_d2pt()
	results = []
	results.append(constant.TLG_CUSTOM_COLUMNS)
	for game in game_list:
		avg_mmr = game[constant.KEYWORD_AVERAGE_MMR]
		game_mode = GAME_MODE[game[constant.KEYWORD_GAME_MODE]]
		game_time = game[constant.KEYWORD_GAME_TIME]
		hour, sec = game_time // 60, game_time % 60
		game_time = str(hour) + ":" +str(sec)
		n_spectators = int(game[constant.KEYWORD_SPECTATORS])
		r_team_name = "Unknown"
		d_team_name = "Unknown"
		gold_lead = f"Radiant:{game[constant.KEYWORD_RADIANT_LEAD]}" if int(game[constant.KEYWORD_RADIANT_LEAD]) > 0\
					  else f"Dire:{abs(int(game[constant.KEYWORD_RADIANT_LEAD]))}"
		r_kills = game[constant.KEYWORD_RADIANT_SCORE]
		d_kills = game[constant.KEYWORD_DIRE_SCORE]
		if constant.KEYWORD_RADIANT_TEAM in game:
			r_team_name = game[constant.KEYWORD_RADIANT_TEAM]
		if constant.KEYWORD_DIRE_TEAM in game:
			d_team_name = game[constant.KEYWORD_DIRE_TEAM]

		match_id = game[constant.KEYWORD_MATCH_ID]
		notable_players = '' if match_id not in notable_player_dict else notable_player_dict[match_id]
		results.append([notable_players, r_team_name, d_team_name, avg_mmr, game_mode, n_spectators,
						game_time, r_kills, d_kills, gold_lead])

	results = [results[0]] + sorted(results[1:], key =lambda x: (x[4]), reverse=True)
	results = results[:length]
	results = pd.DataFrame(results[1:], columns=results[0])
	image_path = render_mpl_table(results, image_path=constant.TLG_IMAGE_PATH, header_columns=0, col_width=2.1,
								  row_height=0.8, title='TOP LIVE GAMES', font_size=13, header_color='#4B4C51',
								  row_colors=['#C0C0C0', '#A9A9A9'])
	# image_path = DataFrame_to_image(results)
	image = cv2.imread(image_path)
	image = image[:, int(image.shape[1]*.09): -(int(image.shape[1]*.07))]
	cv2.imwrite(image_path, image)
	return image_path


if __name__ == '__main__':
	# print(get_notable_hero_from_d2pt())
	path = get_top_games(10)
	print(path)