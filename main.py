# client ID 501100945405378562
# token NTAxMTAwOTQ1NDA1Mzc4NTYy.DqUeoQ.pxwwUuubokrUHgdO2WNFi1uhrFs
# permission 67648

# https://discordapp.com/oauth2/authorize?client_id=501100945405378562&scope=bot&permissions=67648

import discord
import sys
from constant import discord_token, client_id, MAX_MESSAGE_WORD_LENGTH
from applications.signup import signup
from applications.profile_info import profile
from applications.top_games import get_top_games
from web_scrap.scrap import get_current_trend, get_counter_hero, get_good_against
from web_scrap.scrap import get_skill_build, get_item_build

client = discord.Client()

commands_list = {'!top_game'       : 'Shows top 9 Live Games',
                 '!counter HeroName': 'Shows Heroes which counter the given hero name',
                 '!good HeroName'   : '(Opposite of !counter) Shows Heroes which di-counter the given hero name',
                 '!skill or !talent HeroName': 'Shows most popular & win rate talent/skill build',
                 '!item HeroName'   : 'Shows current meta item build by Top Rank Players',
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
    message_string = message.content
    message_string = message_string.lower().strip()
    message_word_length = len(message_string.split())
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    
    if '!help' == message_string:
        help_string = get_help()
        await message.channel.send(help_string)

    elif '!top_game' == message_string or '!top game' == message_string:
        image_path = get_top_games()
        await message.channel.send(f"Getting Top Live Spectacting Games")
        await message.channel.send('Top Games: ', file=discord.File(f'{image_path}'))

    elif '!signup' in message_string and message_word_length < MAX_MESSAGE_WORD_LENGTH:
        result = signup(message_string)
        await message.channel.send(result)

    elif '!profile' in message_string.split()[0]:
        result = profile(message_string)
        await message.channel.send(result)

    elif f"<@!{client_id}>" in message_string:
        await message.channel.send(f"Hello {message.author.name},"
                                   f" Please type    **!help**    for more options")

    elif "!trend" in message_string and message_word_length < (MAX_MESSAGE_WORD_LENGTH - 2):
        image_path = get_current_trend()
        await message.channel.send(f"Getting this week Heroes Trend")
        await message.channel.send('Current Trend: ', file=discord.File(image_path))

    elif ("!counter" in message_string or "!bad" in message_string) and message_word_length < MAX_MESSAGE_WORD_LENGTH:
        found, hero_name, image_path = get_counter_hero(message_string)
        if not found:
            if hero_name != '':
                await message.channel.send(f"Do you mean  **{hero_name}**, Try again with correct name")
            else:
                await message.channel.send(f"Could not find hero, Please make sure the hero name is correct")
        else:
            await message.channel.send(f'**{hero_name.upper()}** is bad against: ', file=discord.File(image_path))

    elif "!good" in message_string and message_word_length < MAX_MESSAGE_WORD_LENGTH:
        found, hero_name, image_path = get_good_against(message_string)
        if not found:
            if hero_name != '':
                await message.channel.send(f"Do you mean  **{hero_name}**, Try again with correct name")
            else:
                await message.channel.send(f"Could not find hero, Please make sure the hero name is correct")
        else:
            await message.channel.send(f'**{hero_name.upper()}** is good against: ', file=discord.File(image_path))

    elif ("!skill" in message_string or "!talent" in message_string) \
            and message_word_length < MAX_MESSAGE_WORD_LENGTH:
        found, hero_name, image_path = await get_skill_build(message_string)
        if not found:
            if hero_name != '':
                await message.channel.send(f"Do you mean  **{hero_name}**, Try again with correct name")
            else:
                await message.channel.send(f"Could not find hero, Please make sure the hero name is correct")
        else:
            await message.channel.send(f'**{hero_name.upper()}** most popular Skill/Talent build: ', file=discord.File(image_path))

    elif "!item" in message_string and message_word_length < MAX_MESSAGE_WORD_LENGTH:
        found, hero_name, image_path = get_item_build(message_string)
        if not found:
            if hero_name != '':
                await message.channel.send(f"Do you mean  **{hero_name}**, Try again with correct name")
            else:
                await message.channel.send(f"Could not find hero, Please make sure the hero name is correct")
        else:
            await message.channel.send(f'**{hero_name.upper()}** recent Item build by **Top Rank Players**:', file=discord.File(image_path))

    elif "exit" in message_string.lower():
        await client.close()
        sys.exit()


client.run(discord_token)
