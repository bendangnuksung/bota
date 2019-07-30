import pandas as pd
import dota2api
from utility import DataFrame_to_image, is_file_old
from constant import GAME_MODE
from private_constant import DOTA2_API_KEY
import constant

dota_api = dota2api.Initialise(DOTA2_API_KEY)


def get_top_games(length=10):
	"""
	Creates a table image of current top live games
	:param length:
	:return: table image path
	"""
	# If TLG image already exist and hasnt been modified in given Threshold second return the same image
	if not is_file_old(constant.TLG_IMAGE_PATH, constant.TLG_IMAGE_UPDATE_TIME_THRESHOLD):
		return constant.TLG_IMAGE_PATH

	game_list = dota_api.get_top_live_games()
	game_list = game_list['game_list']
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
		results.append([r_team_name, d_team_name, avg_mmr, game_mode, n_spectators, game_time, r_kills, d_kills, gold_lead])
	results = [results[0]] + sorted(results[1:], key =lambda x: (x[4]), reverse=True)
	results = results[:length]
	results = pd.DataFrame(results[1:], columns=results[0])
	image_path = DataFrame_to_image(results)
	return image_path