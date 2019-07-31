import discord
import sys
from constant import MAX_COMMAND_WORD_LENGTH
from private_constant import DISCORD_TOKEN, DISCORD_CLIENT_ID, ADMIN_ID
from applications.top_games import get_top_games
from web_scrap.scrap import get_current_trend, get_counter_hero, get_good_against, get_reddit
from web_scrap.scrap import get_skill_build, get_item_build, get_profile, save_id
from web_scrap.twitch_process import get_dota2_top_stream
from discord.utils import find
import constant


client = discord.Client()

commands_list = {'!top_game'        : 'Shows top 9 Live Games        eg: `!top game`',
                 '!counter HeroName': 'Shows Heroes which counter the given hero name        eg: `!counter am`',
                 '!good HeroName'   : 'Opposite of !counter command. Good against.        eg: `!good axe`',
                 '!skill or !talent HeroName': 'Shows most popular & win rate talent/skill build        eg:`!skill meepo`',
                 '!item HeroName'   : 'Shows current meta item build by Top Rank Players        eg: `!item kotl`',
                 '!profile  steamID': 'Shows your profile stats given steamID        eg: `!profile 116585378`',
                 '!save Alias steamID': 'Saves your steamID under Alias name, and call by Alias name.\n'
                                       '        \
                                       First **--->** `!save midone 116585378`  Then **--->** `!profile midone`',
                 '!trend'           : 'Shows current heroes trend        eg: `!trend`',
                 '!twitch'          : 'Shows Top 8 Twitch stream        eg: `!twitch`',
                 '!reddit'          : 'Gets a reddit post from   **/r/DotA2**. You can specify your `SortBy` like below :\n'
                                      '                       eg 1:   `!reddit`             : Gets a random post from  /r/DotA2/\n'
                                      '                       eg 2:   `!reddit hot`   : Gets Top 3 hot post from  /r/DotA2/\n'
                                      '                       eg 3:   `!reddit new`   : Gets Top 3 new post from    /r/DotA2/\n'
                 }


def get_help():
    help_string = []
    head = '```css\nBelow are the commands to use DOTA BOT: 😋```'
    help_string.append(head)
    for key, value in commands_list.items():
        command = '**' + key + '**'
        command_help = '*' + value + '*'
        full = command + '\t:\t' + command_help
        help_string.append(full + '\n')
    help_string = "\n".join(help_string)
    return help_string


@client.event  # event decorator/wrapper
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Dota2 | type '!help'"))
    print(f"Logged in as {client.user}")


@client.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send(f'Hello **{format(guild.name)}**✌✌!\n'
                           f'Type   `!help`   to get list of commands to use.')

@client.event
async def on_message(message):
    message_string = message.content
    message_string = message_string.lower().strip()
    message_word_length = len(message_string.split())
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")

    if client.user == message.author:
        # Ignore all message passed by the our bot
        pass
    
    elif '!help' == message_string or '--help' == message_string:
        help_string = get_help()
        await message.channel.send(help_string)

    elif ('!top_game' in message_string or '!top game' in message_string) and \
         message_word_length < MAX_COMMAND_WORD_LENGTH:
        image_path = get_top_games()
        await message.channel.send(f"Getting Top Live Spectacting Games")
        await message.channel.send('Top Games: ', file=discord.File(f'{image_path}'))

    elif '!profile' in message_string.split()[0]:
        # mode = 0 searching by ID, mode = 1 searching by Alias name(user name)
        flag, id, mode, result = get_profile(message_string)
        if not flag:
            if mode == 1:
                await message.channel.send(f'Could not find any profile under: **{id}**')
            else:
                await message.channel.send(f'Could not find any Alias name : **{id}**')
        else:
            await message.channel.send(f"____**{id}**____'s Profile:")
            await message.channel.send(result)

    elif '!save' in message_string.split()[0]:
        user_name, id, flag, status = save_id(message_string)
        if flag:
            await message.channel.send(f'**{id}** saved under the alias: {user_name}')
        else:
            await message.channel.send(f'**Failed to save, reason: {status}')

    elif "!trend" in message_string and message_word_length < (MAX_COMMAND_WORD_LENGTH - 2):
        image_path = get_current_trend()
        await message.channel.send(f"Getting this week Heroes Trend")
        await message.channel.send('Current Trend: ', file=discord.File(image_path))

    elif ("!counter" in message_string or "!bad" in message_string) and message_word_length < MAX_COMMAND_WORD_LENGTH:
        found, hero_name, image_path = get_counter_hero(message_string)
        if not found:
            if hero_name != '':
                await message.channel.send(f"Do you mean  **{hero_name}**, Try again with correct name")
            else:
                await message.channel.send(f"Could not find hero, Please make sure the hero name is correct")
        else:
            await message.channel.send(f'**{hero_name.upper()}** is bad against: ', file=discord.File(image_path))

    elif "!good" in message_string and message_word_length < MAX_COMMAND_WORD_LENGTH:
        found, hero_name, image_path = get_good_against(message_string)
        if not found:
            if hero_name != '':
                await message.channel.send(f"Do you mean  **{hero_name}**, Try again with correct name")
            else:
                await message.channel.send(f"Could not find hero, Please make sure the hero name is correct")
        else:
            await message.channel.send(f'**{hero_name.upper()}** is good against: ', file=discord.File(image_path))

    elif ("!skill" in message_string or "!talent" in message_string) \
            and message_word_length < MAX_COMMAND_WORD_LENGTH:
        found, hero_name, image_path = await get_skill_build(message_string)
        if not found:
            if hero_name != '':
                await message.channel.send(f"Do you mean  **{hero_name}**, Try again with correct name")
            else:
                await message.channel.send(f"Could not find hero, Please make sure the hero name is correct")
        else:
            await message.channel.send(f'**{hero_name.upper()}** most popular Skill/Talent build: ', file=discord.File(image_path))

    elif "!item" in message_string and message_word_length < MAX_COMMAND_WORD_LENGTH:
        found, hero_name, image_path = get_item_build(message_string)
        if not found:
            if hero_name != '':
                await message.channel.send(f"Do you mean  **{hero_name}**, Try again with correct name")
            else:
                await message.channel.send(f"Could not find hero, Please make sure the hero name is correct")
        else:
            await message.channel.send(f'**{hero_name.upper()}** recent Item build by **Top Rank Players**:', file=discord.File(image_path))

    elif "!twitch" in message_string and message_word_length < MAX_COMMAND_WORD_LENGTH:

        result = get_dota2_top_stream()
        await message.channel.send(result)

    elif "!reddit" in message_string and message_word_length < MAX_COMMAND_WORD_LENGTH:
        result_list, mode = get_reddit(message_string)
        await message.channel.send(f"**REDDIT**  SortBy: **{mode.upper()}**")
        for result in result_list:
            await message.channel.send(result)

    elif f"{DISCORD_CLIENT_ID}" in message_string:
        await message.channel.send(f"Hello {message.author.name}"
                                   f" Please type    `!help`    for more options")

    # Admin privilege
    elif "!get_user" in message_string and str(message.author) == ADMIN_ID:
        await message.channel.send(f'Steam Users ID:', file=discord.File(constant.STEAM_USER_FILE_PATH))

    elif "!exit" in message_string.lower() and str(message.author) == ADMIN_ID:
        await client.close()
        sys.exit()


client.run(DISCORD_TOKEN)
