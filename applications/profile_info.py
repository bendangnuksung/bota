from applications.signup import user
import requests
import json
import os
from constant import rank_tier, COUNTRIES


players_head = "https://api.opendota.com/api/players/"


def get_tier(r_tier):
	first = int(str(r_tier)[0]) -1
	last = int(str(r_tier)[-1]) 
	if first >= len(rank_tier) -1:
		return rank_tier[-1]
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
	if tier is not	 None:
		data['rank_tier']  = get_tier(tier)
	else:
		data['rank_tier']  = 'Uncalibrated'

	time = json_data['profile']['last_login']
	if time is not None:
		data['last_login'] = time[:10] + " " + time[11:19]
	else:
		data['last_login'] = 'Hidden'

	country_code = json_data['profile']['loccountrycode']
	if country_code is not None:
		data['country'] = COUNTRIES[country_code.upper()]
	else:
		data['country'] = 'Hidden'

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


def get_profile(name=None, id=0):
	if not id:
		if not user.user_names.get(name):
			return f"user: {name} not found"
		id = user.user_names[name]
	else:
		id = str(id)
		name = id
	url = os.path.join(players_head, id)
	response = requests.get(url)
	json_data = json.loads(response.text)
	json_data = clean_profile(json_data)
	head = f"{name}'s profile:\n"
	body = ""
	for key, val in json_data.items():
		body += f"**{key}**: *{val}*\n"
	win, lose = get_win_lose(id)
	result = head + body + "**win**: " + str(win) + "\n" + "**lose:** " + str(lose)
	return result


def profile(query):
	query = query.split()
	val = query[1]
	val = val.strip()
	val = eval(val)
	if type(val) == int:
		r = get_profile(id=val)
	else:
		r = get_profile(name=val)
	return r


if __name__ == "__main__":
	print(profile('profile david'))