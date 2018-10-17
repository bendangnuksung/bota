from signup import user
import requests
import json
import os
from constant import rank_tier, COUNTRIES


players_head = "https://api.opendota.com/api/players/"


def get_tier(r_tier):
	first = int(str(r_tier)[0]) -1
	last = int(str(r_tier)[-1]) 
	if first > len(rank_tier):
		return rank_tier[-1] + " 5"
	r = rank_tier[first]
	if last > 5:
		return r + " 5"
	else:
		return r + " " + str(last)


def clean_profile(json_data):
	data = {}
	data['gaming_name'] = json_data['profile']['personaname']
	data['profile_url'] = json_data['profile']['profileurl']
	tier = json_data['rank_tier']
	data['rank_tier']  = get_tier(tier)
	time = json_data['profile']['last_login']
	data['last_login'] = time[:10] + " " + time[11:19]
	country_code = json_data['profile']['loccountrycode']
	data['country'] = COUNTRIES[country_code.upper()]
	data['mmr_estimate'] = json_data['mmr_estimate']['estimate']
	data['competitive_rank'] = json_data['competitive_rank']
	return data


def get_win_lose(id):
	url = players_head + id + "/wl"
	response = requests.get(url)
	data = json.loads(response.text)
	win = data['win']
	lose = data['lose']
	return win, lose


def get_profile(name):
	if not user.user_names.get(name):
		return f"user: {name} not found"
	id = user.user_names[name]
	url = os.path.join(players_head, id)
	response = requests.get(url)
	json_data = json.loads(response.text)
	json_data = clean_profile(json_data)
	head = f"{name}'s profile:\n"
	body = ""
	for key, val in json_data.items():
		body += f"{key}: {val}\n"
	win, lose = get_win_lose(id)
	result = head + body + "win: " + str(win) + "\n" + "lose: " + str(lose)
	return result


def profile(query):
	query = query.split(' ')
	name = query[1]
	r = get_profile(name)
	return r


if __name__ == "__main__":
	print(profile('profile david'))