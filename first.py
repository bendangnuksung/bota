# client ID 501100945405378562
# token NTAxMTAwOTQ1NDA1Mzc4NTYy.DqUeoQ.pxwwUuubokrUHgdO2WNFi1uhrFs
# permission 67648

# https://discordapp.com/oauth2/authorize?client_id=501100945405378562&scope=bot&permissions=67648

import discord
import sys
from constant import discord_token
from applications.signup import signup
from applications.profile_info import profile
from applications.top_games import get_top_games

client = discord.Client()

commands_list = {'!top_games': 'Shows top 9 Live Games',
                 '!signup  username  steamID': 'Registers your steamID with the username for fast profile view',
                 '!profile  username': 'Shows your profile stats with the registered username',
                 '!profile  steamID': 'Shows your profile stats given steamID'}


def get_help():
    help_string = []
    head = '**Below are the commands to use DOTA BOT:**\n'
    help_string.append(head)
    for key, value in commands_list.items():
        command = '**' + key + '**'
        command_help = '*' + value + '*'
        full = command + '\t:\t' + command_help
        help_string.append(full)
    help_string = "\n".join(help_string)
    return help_string


@client.event  # event decorator/wrapper
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")

    if '!help' == message.content:
        help_string = get_help()
        await message.channel.send(help_string)

    elif '!top_games' == message.content:
        result = get_top_games()
        await message.channel.send(f"Getting Top Live Spectacting Games")
        await message.channel.send('Top Games: ', file=discord.File(f'{result}'))

    elif '!signup' in message.content:
        result = signup(message.content)
        await message.channel.send(result)

    elif '!profile' in message.content.split()[0]:
        result = profile(message.content)
        await message.channel.send(result)

    elif "@dota_info" in message.content.lower():
        await message.channel.send(f"Hello {message.author.name}")

    elif "exit" in message.content.lower():
        await client.close()
        sys.exit()


client.run(discord_token)
