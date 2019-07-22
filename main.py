# client ID 501100945405378562
# token NTAxMTAwOTQ1NDA1Mzc4NTYy.DqUeoQ.pxwwUuubokrUHgdO2WNFi1uhrFs
# permission 67648

# https://discordapp.com/oauth2/authorize?client_id=501100945405378562&scope=bot&permissions=67648

import discord
import sys
from constant import discord_token, client_id
from applications.signup import signup
from applications.profile_info import profile
from applications.top_games import get_top_games
from web_scrap.scrap import get_current_trend, get_counter_hero, get_good_against
from web_scrap.scrap import get_skill_build

client = discord.Client()

commands_list = {'!top_games'       : 'Shows top 9 Live Games',
                 '!counter HeroName': 'Shows Heroes which counter the given hero name',
                 '!good HeroName'   : '(Opposite of !counter) Shows Heroes which di-counter the given hero name',
                 '!skill or !talent or !build HeroName': 'Shows most popular & win rate talent/skill build',
                 '!profile  steamID': 'Shows your profile stats given steamID',
                 '!trend'           : 'Shows current heroes trend',
                 }


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
        image_path = get_top_games()
        await message.channel.send(f"Getting Top Live Spectacting Games")
        await message.channel.send('Top Games: ', file=discord.File(f'{image_path}'))

    elif '!signup' in message.content:
        result = signup(message.content)
        await message.channel.send(result)

    elif '!profile' in message.content.split()[0]:
        result = profile(message.content)
        await message.channel.send(result)

    elif f"<@!{client_id}>" in message.content:
        await message.channel.send(f"Hello {message.author.name},"
                                   f" Please type    **!help**    for more options")

    elif "!trend" in message.content:
        image_path = get_current_trend()
        await message.channel.send(f"Getting this week Heroes Trend")
        await message.channel.send('Current Trend: ', file=discord.File(image_path))

    elif "!counter" in message.content:
        found, hero_name, image_path = get_counter_hero(message.content)
        if not found:
            if hero_name != '':
                await message.channel.send(f"Do you mean  **{hero_name}**, Try again with correct name")
            else:
                await message.channel.send(f"Could not find hero, Please make sure the hero name is correct")
        else:
            await message.channel.send(f'**{hero_name}** is bad against: ', file=discord.File(image_path))

    elif "!good" in message.content:
        found, hero_name, image_path = get_good_against(message.content)
        if not found:
            if hero_name != '':
                await message.channel.send(f"Do you mean  **{hero_name}**, Try again with correct name")
            else:
                await message.channel.send(f"Could not find hero, Please make sure the hero name is correct")
        else:
            await message.channel.send(f'**{hero_name}** is good against: ', file=discord.File(image_path))

    elif "!skill" in message.content or "!talent" in message.content or "!build" in message.content:
        found, hero_name, image_path = await get_skill_build(message.content)
        if not found:
            if hero_name != '':
                await message.channel.send(f"Do you mean  **{hero_name}**, Try again with correct name")
            else:
                await message.channel.send(f"Could not find hero, Please make sure the hero name is correct")
        else:
            await message.channel.send(f'**{hero_name}** most popular Skill/Talent build: ', file=discord.File(image_path))

    elif "exit" in message.content.lower():
        await client.close()
        sys.exit()


client.run(discord_token)
