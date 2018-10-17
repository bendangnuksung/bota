# client ID 501100945405378562
# token NTAxMTAwOTQ1NDA1Mzc4NTYy.DqUeoQ.pxwwUuubokrUHgdO2WNFi1uhrFs
# permission 67648

# https://discordapp.com/oauth2/authorize?client_id=501100945405378562&scope=bot&permissions=67648

import discord
import sys
import dota2api
import pandas as pd
from panda_to_image import DataFrame_to_image
from constant import dota2_api_key, GAME_MODE, discord_token
from signup import signup
from profile_info import profile


dota_api = dota2api.Initialise(dota2_api_key)


client = discord.Client()


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


@client.event # event decorator/wrapper
async def on_ready():
	print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
	print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")

	if 'member_count' == message.content:
		for guild in guilds:
			guild = client.get_guild(guild)
			await message.channel.send(f"{guild.name}: {guild.member_count}")

	elif 'top_games' == message.content:
		result = get_top_games()
		await message.channel.send(f"Getting Top Live Spectacting Games")
		await message.channel.send('Top Games: ', file=discord.File(f'{result}'))

	elif 'signup' in message.content:
		result = signup(message.content)
		await message.channel.send(result)

	elif 'profile' in message.content.split()[0]:
		result = profile(message.content)
		await message.channel.send(result)		

	elif "hi dota_info" in message.content.lower():
		await message.channel.send(f"Hello {message.author.name}")

	elif "exit" in message.content.lower():
		await client.close()
		sys.exit()


client.run(discord_token)
