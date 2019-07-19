import pandas as pd
import dota2api
from utility import DataFrame_to_image
from constant import GAME_MODE, dota2_api_key

dota_api = dota2api.Initialise(dota2_api_key)


def get_top_games(length=10):
	game_list = dota_api.get_top_live_games()
	game_list = game_list['game_list']
	results = []
	results.append(['Radiant', 'Dire', 'Avg MMR', 'Game Mode', 'Spectators', 'Time', 'R Kills', 'D Kills', 'Gold Lead'])
	for game in game_list:
		avg_mmr = game['average_mmr']
		game_mode = GAME_MODE[game['game_mode']]
		game_time = game['game_time']
		hour, sec = game_time // 60, game_time % 60
		game_time = str(hour) + ":" +str(sec)
		n_spectators = int(game['spectators'])
		r_team_name = "Unknown"
		d_team_name = "Unknown"
		gold_lead = f"Radiant:{game['radiant_lead']}" if int(game['radiant_lead']) > 0 else f"Dire:{abs(int(game['radiant_lead']))}"
		r_kills = game['radiant_score']
		d_kills = game['dire_score']
		if 'team_name_radiant' in game:
			r_team_name = game['team_name_radiant']
		if 'team_name_dire' in game:
			d_team_name = game['team_name_dire']
		results.append([r_team_name, d_team_name, avg_mmr, game_mode, n_spectators, game_time, r_kills, d_kills, gold_lead])
	results = [results[0]] + sorted(results[1:], key =lambda x: (x[4]), reverse=True)
	results = results[:length]
	results = pd.DataFrame(results[1:], columns=results[0])
	result = DataFrame_to_image(results)
	return result