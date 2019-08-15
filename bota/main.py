import discord
import sys
from bota.constant import MAX_COMMAND_WORD_LENGTH, DOTA2_LOGO_URL
from bota.help import HELP_FOOTER, LAST_UPDATE, get_help
from bota.private_constant import DISCORD_TOKEN, DISCORD_CLIENT_ID, ADMIN_ID
from bota.applications.top_games import get_top_games
from bota.web_scrap.scrap import get_current_trend, get_counter_hero, get_good_against, get_reddit
from bota.web_scrap.scrap import get_skill_build, get_item_build, get_profile, save_id, get_protracker_hero
from bota.web_scrap.twitch_process import get_dota2_top_stream
from bota.web_scrap.TI import group_stage, help, stats
from bota.log_process import save_command_logs, get_command_log_tail
from discord.utils import find
from bota import constant

client = discord.Client()
GUILDS = []


def is_command_called_correctly(message, minlength, maxlength=constant.MAX_COMMAND_WORD_LENGTH, ):
    pass


def embed_txt_message(content, add_header=False, header=constant.DEFAULT_EMBED_HEADER, color=discord.Color.blue()):
    embed_msg = discord.Embed(description=content, color=color)
    if add_header:
        embed_msg.set_author(name=header['name'], icon_url=header['icon_url'], url=header['url'])
    return embed_msg


async def broadcast_message(msg):
    global GUILDS
    for guild in GUILDS:
        await guild.text_channels[0].send(msg)


@client.event  # event decorator/wrapper
async def on_ready():
    global GUILDS
    GUILDS = client.guilds
    await client.change_presence(activity=discord.Game(name="Dota2 | type '!help'"))
    print(f"Logged in as {client.user}")


@client.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general', guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send(f'Hello **{format(guild.name)}**✌✌!\n'
                           f'Type   `!help` or `!command`   to get list of commands to use.')


# Where the commands gets executed
@client.event
async def on_message(message):
    is_command_called = True
    command_called = ""
    message_string = message.content
    message_string = message_string.lower().strip()
    message_word_length = len(message_string.split())
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")

    # Ignore all message passed by the our bot
    if client.user == message.author:
        is_command_called = False

    # Ignore if message is from another Bot
    elif message.author.bot:
        is_command_called = False

    elif '!help' == message_string or '--help' == message_string or '!command' in message_string:
        command_called = "!help"
        help_string = get_help()
        embed_msg = embed_txt_message(help_string, add_header=True)
        embed_msg.set_footer(text=HELP_FOOTER, icon_url=DOTA2_LOGO_URL)
        await  message.channel.send(embed=embed_msg)

    elif ('!top_game' in message_string or '!top game' in message_string) and \
            message_word_length < MAX_COMMAND_WORD_LENGTH:
        command_called = "!top_game"
        async with message.channel.typing():
            image_path = get_top_games()
            await message.channel.send(f"Getting Top Live Spectacting Games, Source: Dota2API, Dota2ProTracker")
            await message.channel.send('Top Games: ', file=discord.File(f'{image_path}'))

    elif '!profile' in message_string and message_word_length < MAX_COMMAND_WORD_LENGTH:
        if message_word_length == 1:
            msg = f'Please provide a STEAM ID or saved Username: eg: `!profile 116585378`'
            await message.channel.send(msg)
            return
        command_called = "!profile"
        async with message.channel.typing():
            flag, id, mode, result, medal_url = get_profile(message_string)
        result_embed = embed_txt_message(result)
        result_embed.set_author(name=f"**Profile: {id}**", url=f'{constant.PLAYER_URL_BASE}{id}',
                                icon_url=constant.DEFAULT_EMBED_HEADER['icon_url'])
        result_embed.set_thumbnail(url=medal_url)
        if not flag:
            if mode == 1:
                msg = f'Could not find any profile under: **{id}**'
                await message.channel.send(msg)
            else:
                msg = f'Could not find any Alias name : **{id}**, make sure you have saved your profile\n'
                msg += f'You can save your profile using  `!save YourUserName SteamID` eg: `!save midone 116585378`'
                await message.channel.send(msg)
        else:
            await message.channel.send(embed=result_embed)

    elif '!save' in message_string.split()[0]:
        command_called = "!save"
        async with message.channel.typing():
            user_name, id, flag, status = save_id(message_string)
        if flag:
            await message.channel.send(f'**{id}** saved under the alias: {user_name}')
        else:
            await message.channel.send(f'**Failed to save, reason: {status}')

    elif "!trend" in message_string and message_word_length < (MAX_COMMAND_WORD_LENGTH - 2):
        command_called = "!trend"
        async with message.channel.typing():
            image_path = get_current_trend()
            await message.channel.send(f"Getting this week Heroes Trend, Source: DotaBuff")
            embed_msg = discord.Embed(description='Current Trend: ')
            await message.channel.send(embed=embed_msg, file=discord.File(image_path))

    elif ("!counter" in message_string or "!bad" in message_string) and message_word_length < MAX_COMMAND_WORD_LENGTH:
        command_called = "!counter"
        async with message.channel.typing():
            note = f"\n**NOTE**: Can use short Hero Names, `!counter anti mage`   as   `!counter am`"
            found, hero_name, image_path = get_counter_hero(message_string)
            if not found:
                if hero_name != '':
                    await message.channel.send(f"Do you mean  **{hero_name}**, Try again with correct name {note}")
                else:
                    await message.channel.send(f"Could not find hero, Please make sure the hero name is correct {note}")
            else:
                await message.channel.send(f'**{hero_name.upper()}** is bad against, Source: DotaBuff {note}',
                                           file=discord.File(image_path))

    elif "!good" in message_string and message_word_length < MAX_COMMAND_WORD_LENGTH:
        command_called = "!good"
        async with message.channel.typing():
            note = f"\n**NOTE**: Can use short Hero Names, `!counter shadow fiend`   as   `!counter sf`"
            found, hero_name, image_path = get_good_against(message_string)
            if not found:
                if hero_name != '':
                    await message.channel.send(f"Do you mean  **{hero_name}**, Try again with correct name{note}")
                else:
                    await message.channel.send(f"Could not find hero, Please make sure the hero name is correct{note}")
            else:
                await message.channel.send(f'**{hero_name.upper()}** is good against, Source: DotaBuff {note}',
                                           file=discord.File(image_path))

    elif ("!skill" in message_string or "!talent" in message_string) \
            and message_word_length < MAX_COMMAND_WORD_LENGTH:
        command_called = "!skill"
        async with message.channel.typing():
            note = f"\n**NOTE**: Can use short Hero Names, `!counter queen of pain`   as   `!counter qop`"
            found, hero_name, image_path = await get_skill_build(message_string)
            if not found:
                if hero_name != '':
                    await message.channel.send(f"Do you mean  **{hero_name}**, Try again with correct name{note}")
                else:
                    await message.channel.send(f"Could not find hero, Please make sure the hero name is correct{note}")
            else:
                await message.channel.send(
                    f'**{hero_name.upper()}** most popular Skill/Talent build: , Source: DotaBuff{note}',
                    file=discord.File(image_path))

    elif "!item" in message_string and message_word_length < MAX_COMMAND_WORD_LENGTH:
        command_called = "!item"
        async with message.channel.typing():
            note = f"\n**NOTE**: Can use short Hero Names, `!counter dragon knight`   as   `!counter dk`"
            found, hero_name, image_path = get_item_build(message_string)
            if not found:
                if hero_name != '':
                    await message.channel.send(f"Do you mean  **{hero_name}**, Try again with correct name{note}")
                else:
                    await message.channel.send(f"Could not find hero, Please make sure the hero name is correct{note}")
            else:
                await message.channel.send(
                    f'**{hero_name.upper()}** recent Item build by **Top Rank Players**:, Source: DotaBuff{note}',
                    file=discord.File(image_path))

    elif "!twitch" in message_string and message_word_length < MAX_COMMAND_WORD_LENGTH:
        command_called = "!twitch"
        async with message.channel.typing():
            language = None if len(message_string.split()) <= 1 else message_string.split()[1]
            result = get_dota2_top_stream(language)
        embed_msg = embed_txt_message(result)
        await message.channel.send(embed=embed_msg)

    elif "!reddit" in message_string and message_word_length < MAX_COMMAND_WORD_LENGTH:
        async with message.channel.typing():
            result_list, mode = get_reddit(message_string)
        command_called = f"!reddit {mode}"
        await message.channel.send(f"**REDDIT**  SortBy: **{mode.upper()}**, Source: Reddit")
        for result in result_list:
            await message.channel.send(f'{result}')

    elif "!pro" in message_string and message_word_length < MAX_COMMAND_WORD_LENGTH:
        command_called = "!protrack"
        async with message.channel.typing():
            found, hero_name, result_string, icon_path = get_protracker_hero(message_string)
        if not found:
            if hero_name != '':
                await message.channel.send(f"Do you mean  **{hero_name}**, Try again with correct name")
            else:
                await message.channel.send(f"Could not find hero, Please make sure the hero name is correct")
        else:
            embed_msg = embed_txt_message(result_string)
            embed_msg.set_author(name=f'**{hero_name.upper()}** Dota2ProTracker:', url=constant.D2PT_WEBSITE_URL,
                                 icon_url=f'{constant.CHARACTER_ICONS_URL}{hero_name}.png')
            embed_msg.set_thumbnail(url=f'{constant.CHARACTER_ICONS_URL}{hero_name}.png')
            await message.channel.send(embed=embed_msg)

    elif "!ti" in message_string:
        command_called = '!ti'
        message_split = message_string.split()
        if len(message_split) > 1 and 'group' in message_split[1]:
            async with message.channel.typing():
                command_called = '!ti group'
                result_string = group_stage.get_group_stage()
            result_string = embed_txt_message(result_string, color=discord.Color.purple())
            result_string.set_thumbnail(url=constant.TI_LOGO_URL)
            result_string.set_author(name='TI9 GROUP STAGE')
            await message.channel.send(embed=result_string)

        elif len(message_split) > 1 and 'stat' in message_split[1]:
            async with message.channel.typing():
                command_called = '!ti stat'
                result_string = stats.get_all_stats()
            result_string = embed_txt_message(result_string, color=discord.Color.purple())
            result_string.set_thumbnail(url=constant.TI_LOGO_URL)
            result_string.set_author(name='TI9 Hero Stats')
            await message.channel.send(embed=result_string)

        else:
            result_string = help.help_message
            result_string = embed_txt_message(result_string, color=discord.Color.purple())
            result_string.set_thumbnail(url=constant.TI_LOGO_URL)
            result_string.set_author(name='TI9 COMMANDS')
            await message.channel.send(embed=result_string)

    elif "!update" in message_string and message_word_length < 2:
        await message.channel.send(LAST_UPDATE)

    # Admin privilege
    elif "!get_user" in message_string and str(message.author) == ADMIN_ID:
        command_called = "!get_user"
        await message.channel.send(f'Steam Users ID:', file=discord.File(constant.STEAM_USER_FILE_PATH))

    elif "!exit" in message_string and str(message.author) == ADMIN_ID:
        message_split = message_string.split()
        if len(message_split) > 1:
            client_id = message_split[1]
            if str(client_id) == str(DISCORD_CLIENT_ID):
                await message.channel.send(f'Exiting client: {client_id}')
                sys.exit(0)

    elif "!broadcast" in message_string and str(message.author) == ADMIN_ID:
        async with message.channel.typing():
            message_split = message_string.split()
            if len(message_split) > 1:
                client_id = message_split[1]
                if str(client_id) == str(DISCORD_CLIENT_ID):
                    message = " ".join(message_split[2:])
                    await broadcast_message(message)

    elif "!tail" in message_string and str(message.author) == ADMIN_ID:
        is_command_called = False
        n = 5
        try:
            n = int(message_string.split()[1])
        except Exception:
            pass
        tail_log = get_command_log_tail(n)
        await message.channel.send(tail_log)

    # Message user
    elif f"{DISCORD_CLIENT_ID}" in message_string:
        await message.channel.send(f"Hello {message.author.name}"
                                   f" Please type    `!help`  or `!command`  for more options")

    else:
        is_command_called = False

    if is_command_called:
        save_command_logs(message, command_called)


client.run(DISCORD_TOKEN)