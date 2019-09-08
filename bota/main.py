import discord
import sys
from bota.constant import MAX_COMMAND_WORD_LENGTH, DOTA2_LOGO_URL
from bota.help import HELP_FOOTER, LAST_UPDATE, get_help, PROFILE_HELP_STRING, NOTE_FOOTER, TEAM_CMD_EXAMPLE, BOTA_SUPPORT_SERVER_URL, BOTA_ADD_TO_SERVER_URL
from bota.private_constant import DISCORD_TOKEN, DISCORD_CLIENT_ID, ADMIN_ID
from bota.applications.top_games import get_top_games
from bota.web_scrap.scrap import get_current_trend, get_counter_hero, get_good_against, get_reddit, save_id_in_db
from bota.web_scrap.scrap import get_skill_build, get_item_build, get_profile_from_db, get_protracker_hero
from bota.web_scrap.twitch_process import get_dota2_top_stream
from bota.web_scrap.TI import group_stage, help, stats, matches
from bota.log_process import save_command_logs, get_command_log_tail
from bota.web_scrap.dotavoyance.getter import get_team_mate
from discord.utils import find
from bota import constant
import os

client = discord.AutoShardedClient()
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


def add_footer_requested_by_username(embed, message, note=NOTE_FOOTER):
    try:
        user_discord_id = message.author.id
        user = message.guild.get_member(user_discord_id)
        embed.set_footer(text=f'Req by {message.author.name}{note}', icon_url=user.avatar_url)
        return embed
    except Exception as e:
        return embed


#################################################################################################
"""
Below lies the Definition of all commands from on_message()
"""


async def cmd_help(message):
    command_called = '!help'
    help_string = get_help()
    embed_msg = embed_txt_message(help_string, add_header=True)
    embed_msg.set_footer(text=HELP_FOOTER, icon_url=DOTA2_LOGO_URL)
    embed_msg.add_field(name="Help and Support", value=(f"Add BOTA to your server: **[Click here]({BOTA_ADD_TO_SERVER_URL})**\n"
                                        f"Join BOTA support server for more help: **[Click here]({BOTA_SUPPORT_SERVER_URL})**"))
    await  message.channel.send(embed=embed_msg)
    return True, command_called


async def cmd_top_game(message):
    command_called = '!top game'
    async with message.channel.typing():
        image_path = get_top_games()
        msg = "Top Live Games: Dota2API, Dota2ProTracker"
        embed = discord.Embed(color=discord.Color.green())
        embed.title = msg
        image_file = discord.File(image_path, os.path.basename(image_path))
        embed.add_field(name="Source:", value=('[Dota2API](https://demodota2api.readthedocs.io/en/latest/#)  '
                                               '[Dota2ProTracker](http://www.dota2protracker.com)'))
        embed.set_image(url=f"attachment://{image_file.filename}")
        embed = add_footer_requested_by_username(embed, message)
        await message.channel.send(embed=embed, file=image_file)
    return True, command_called


async def cmd_trend(message):
    command_called = '!trend'
    async with message.channel.typing():
        image_path = get_current_trend()
        msg = "Current Heroes Trend"
        desc = "Weekly Heroes Trend: Win Rate and Pick Rate"
        embed = discord.Embed(description=desc, color=discord.Color.green())
        embed.title = msg
        image_file = discord.File(image_path, os.path.basename(image_path))
        embed.add_field(name="Source:", value=('[DotaBuff](https://www.dotabuff.com/heroes/trends)'))
        embed.set_image(url=f"attachment://{image_file.filename}")
        embed = add_footer_requested_by_username(embed, message)
        await message.channel.send(embed=embed, file=image_file)
    return True, command_called


async def cmd_reddit(message, message_string):
    async with message.channel.typing():
        result_list, mode = get_reddit(message_string)
    command_called = f"!reddit {mode}"
    await message.channel.send(f"**REDDIT**  SortBy: **{mode.upper()}**, Source: Reddit")
    for result in result_list:
        await message.channel.send(f'{result}')
    return True, command_called


async def cmd_protracker(message, message_string):
    command_called = '!protrack'
    async with message.channel.typing():
        found, hero_name, result_string, icon_path = get_protracker_hero(message_string)
    if not found:
        if hero_name != '':
            await message.channel.send(f"Do you mean  **{hero_name}**, Try again with correct name")
        else:
            await message.channel.send(f"Could not find hero, Please make sure the hero name is correct")
        return False, command_called
    else:
        embed_msg = embed_txt_message(result_string)
        embed_msg.set_author(name=f'**{hero_name.upper()}** Dota2ProTracker:', url=constant.D2PT_WEBSITE_URL,
                             icon_url=f'{constant.CHARACTER_ICONS_URL}{hero_name}.png')
        embed_msg.set_thumbnail(url=f'{constant.CHARACTER_ICONS_URL}{hero_name}.png')
        embed_msg = add_footer_requested_by_username(embed_msg, message)
        await message.channel.send(embed=embed_msg)
        return True, command_called


async def cmd_counter(message, message_string):
    command_called = '!counter'
    async with message.channel.typing():
        note = f'Can save your profile without name and change Steam ID and others, Type **`!profile help`** for details'
        found, hero_name, image_path = get_counter_hero(message_string)
        if not found:
            if hero_name != '':
                msg = f"Do you mean  **{hero_name}**, Try again with correct name"
                msg = embed_txt_message(msg, color=discord.Color.red())
                await message.channel.send(embed=msg)
            else:
                msg = f"Could not find hero, Please make sure the hero name is correct"
                msg = embed_txt_message(msg, color=discord.Color.red())
                await message.channel.send(embed=msg)
            return False, command_called
        else:
            desc = f'**{hero_name.upper()}** is bad against, **Source**: [DotaBuff](https://www.dotabuff.com/heroes/{hero_name}/counters)'
            title = f"{hero_name.upper()} is countered by:"
            embed = discord.Embed(description=desc, color=discord.Color.red(), title=title)
            image_file = discord.File(image_path, os.path.basename(image_path))
            embed.set_image(url=f"attachment://{image_file.filename}")
            embed.add_field(name="Update:", value=(note))
            embed = add_footer_requested_by_username(embed, message)
            await message.channel.send(embed=embed, file=image_file)
            return True, command_called


async def cmd_item(message, message_string):
    command_called = '!item'
    async with message.channel.typing():
        note = f'Can save your profile without name and change Steam ID and others, Type **`!profile help`** for details'
        found, hero_name, image_path = get_item_build(message_string)
        if not found:
            if hero_name != '':
                msg = f"Do you mean  **{hero_name}**, Try again with correct name"
                msg = embed_txt_message(msg, color=discord.Color.red())
                await message.channel.send(embed=msg)
            else:
                msg = f"Could not find hero, Please make sure the hero name is correct"
                msg = embed_txt_message(msg, color=discord.Color.red())
                await message.channel.send(embed=msg)
            return False, command_called
        else:
            desc = f'**{hero_name.upper()}** recent Item build by **Top Rank Players**:, [DotaBuff](https://www.dotabuff.com/heroes/{hero_name}/guides)'
            title = f"{hero_name.upper()} Item Build:"
            embed = discord.Embed(description=desc, color=discord.Color.blurple(), title=title)
            image_file = discord.File(image_path, os.path.basename(image_path))
            embed.set_image(url=f"attachment://{image_file.filename}")
            embed.add_field(name="Update:", value=(note))
            embed = add_footer_requested_by_username(embed, message)
            await message.channel.send(embed=embed, file=image_file)
            return True, command_called


async def cmd_good(message, message_string):
    command_called = '!good'
    async with message.channel.typing():
        note = f'Can save your profile without name and change Steam ID and others, Type **`!profile help`** for details'
        found, hero_name, image_path = get_good_against(message_string)
        if not found:
            if hero_name != '':
                msg = f"Do you mean  **{hero_name}**, Try again with correct name "
                msg = embed_txt_message(msg, color=discord.Color.red())
                await message.channel.send(embed=msg)
            else:
                msg = f"Could not find hero, Please make sure the hero name is correct"
                msg = embed_txt_message(msg, color=discord.Color.red())
                await message.channel.send(embed=msg)
            return False, command_called
        else:
            desc = f'**{hero_name.upper()}** is good against, **Source**: [DotaBuff](https://www.dotabuff.com/heroes/{hero_name}/counters)'
            title = f"{hero_name.upper()} counters:"
            embed = discord.Embed(description=desc, color=discord.Color.green(), title=title)
            image_file = discord.File(image_path, os.path.basename(image_path))
            embed.set_image(url=f"attachment://{image_file.filename}")
            embed.add_field(name="Update:", value=(note))
            embed = add_footer_requested_by_username(embed, message)
            await message.channel.send(embed=embed, file=image_file)
            return True, command_called


async def cmd_skill(message, message_string):
    command_called = '!skill'
    async with message.channel.typing():
        note = f'Can save your profile without name and change Steam ID and others, Type **`!profile help`** for details'
        found, hero_name, image_path = await get_skill_build(message_string)
        if not found:
            if hero_name != '':
                msg = f"Do you mean  **{hero_name}**, Try again with correct name"
                msg = embed_txt_message(msg, color=discord.Color.red())
                await message.channel.send(embed=msg)
            else:
                msg = f"Could not find hero, Please make sure the hero name is correct"
                msg = embed_txt_message(msg, color=discord.Color.red())
                await message.channel.send(embed=msg)
            return False, command_called
        else:
            desc = f'**{hero_name.upper()}** most popular Skill/Talent build, **Source**: [DotaBuff](https://www.dotabuff.com/heroes/{hero_name})'
            title = f"{hero_name.upper()} Skill/Talent buildt:"
            embed = discord.Embed(description=desc, color=discord.Color.blurple(), title=title)
            image_file = discord.File(image_path, os.path.basename(image_path))
            embed.set_image(url=f"attachment://{image_file.filename}")
            embed.add_field(name="Update:", value=(note))
            embed = add_footer_requested_by_username(embed, message)
            await message.channel.send(embed=embed, file=image_file)
            return True, command_called


async def cmd_twitch(message, message_string):
    command_called = '!twitch'
    async with message.channel.typing():
        language = None if len(message_string.split()) <= 1 else message_string.split()[1]
        result = get_dota2_top_stream(language)
    embed_msg = embed_txt_message(result)
    embed_msg = add_footer_requested_by_username(embed_msg, message)
    await message.channel.send(embed=embed_msg)
    return True, command_called


async def cmd_save(message, message_string, message_word_length, user_discord_id, user_discord_name):
    if message_word_length == 2 and ('help' == message_string.split()[1] or 'helps' == message_string.split()[1]):
        result_embed = embed_txt_message(PROFILE_HELP_STRING, color=discord.Color.red())
        result_embed.set_author(name="Save Command Help")
        result_embed.set_thumbnail(url=constant.DEFAULT_EMBED_HEADER['icon_url'])
        await message.channel.send(embed=result_embed)
        return
    async with message.channel.typing():
        flag, summary = save_id_in_db(user_discord_id, user_discord_name, message_string)
    if not flag:
        summary = embed_txt_message(summary, color=discord.Color.red())
    else:
        summary = embed_txt_message(summary, color=discord.Color.green())
    summary = add_footer_requested_by_username(summary, message)
    await message.channel.send(embed=summary)


async def cmd_profile(message, message_string, message_word_length, user_discord_id):
    command_called = '!profile'
    if message_word_length == 2 and ('help' == message_string.split()[1] or 'helps' == message_string.split()[1]):
        result_embed = embed_txt_message(PROFILE_HELP_STRING, color=discord.Color.dark_blue())
        result_embed.set_author(name="Profile Command Help")
        result_embed.set_thumbnail(url=constant.DEFAULT_EMBED_HEADER['icon_url'])
        await message.channel.send(embed=result_embed)
        return True, command_called

    async with message.channel.typing():
        try:
            flag, mode, steam_id, alias_name, result, medal_url, dp_url = get_profile_from_db(user_discord_id, message_string)
        except:
            msg = 'Could not fetch your profile. Please make sure your profile is public'
            msg = embed_txt_message(msg, color=discord.Color.red())
            await message.channel.send(embed=msg)
            return False, command_called

    result_embed = embed_txt_message(result, color=discord.Color.green())
    result_embed.set_author(name=f"**Profile: {steam_id}**", url=f'{constant.PLAYER_URL_BASE}{steam_id}',
                            icon_url=dp_url)
    result_embed.set_thumbnail(url=medal_url)
    if not flag:
        if mode == 1:
            msg = f'<@{user_discord_id}> Please save your Steam ID to get your profile, To save your profile:' \
                  f' **`!save SteamID`** eg: **`!save 311360822`**\nPlease type  **`!profile help`**  for more help'
            msg = embed_txt_message(msg, color=discord.Color.red())
            await message.channel.send(embed=msg)
        elif mode == 2:
            msg = f'<@{user_discord_id}> Could not find any profile under the Steam ID:    **{steam_id}**\n' \
                  f'Please type  **`!profile help`**  for more help'
            msg = embed_txt_message(msg, color=discord.Color.red())
            await message.channel.send(embed=msg)
        else:
            msg = f'<@{user_discord_id}> Could not find User:   **{alias_name}**,  You can save a username by eg: ' \
                  f' **`!save {alias_name} SteamID`** \nPlease type  **`!profile help`**  for more help'
            msg = embed_txt_message(msg, color=discord.Color.red())
            await message.channel.send(embed=msg)
        return False, command_called
    else:
        result_embed = add_footer_requested_by_username(result_embed, message)
        await message.channel.send(embed=result_embed)
        return True, command_called


async def cmd_ti(message, message_string):
    message_split = message_string.split()
    if len(message_split) > 1 and 'group' in message_split[1]:
        async with message.channel.typing():
            command_called = '!ti group'
            result_string = group_stage.get_group_stage()
            result_string = 'Type **`!ti main`** to get TI Main Stage bracket and schedule\n' + result_string
        result_string = embed_txt_message(result_string, color=discord.Color.purple())
        result_string.set_thumbnail(url=constant.TI_LOGO_URL)
        result_string.set_author(name='TI9 GROUP STAGE')
        result_string = add_footer_requested_by_username(result_string, message)
        await message.channel.send(embed=result_string)

    elif len(message_split) > 1 and 'stat' in message_split[1]:
        async with message.channel.typing():
            command_called = '!ti stat'
            result_string = stats.get_all_stats()
        result_string = embed_txt_message(result_string, color=discord.Color.purple())
        result_string.set_thumbnail(url=constant.TI_LOGO_URL)
        result_string.set_author(name='TI9 Hero Stats')
        result_string = add_footer_requested_by_username(result_string, message)
        await message.channel.send(embed=result_string)

    elif len(message_split) > 1 and 'match' in message_split[1]:
        result_string = "Could not fetch Upcoming matches\nType  **`!ti main`** to get TI Main Stage bracket and schedule"
        async with message.channel.typing():
            try:
                command_called = '!ti match'
                result_string = matches.get_all_matches()
            except Exception:
                pass
        await message.channel.send(result_string)

    elif len(message_split) > 1 and 'main' in message_split[1]:
        async with message.channel.typing():
            command_called = '!ti main'
            result_string = group_stage.get_main_stage()
        result_string = embed_txt_message(result_string, color=discord.Color.purple())
        result_string.set_thumbnail(url=constant.TI_LOGO_URL)
        result_string.set_author(name='TI9 Main Stage Schedule')
        result_string = add_footer_requested_by_username(result_string, message)
        await message.channel.send(embed=result_string)

    else:
        result_string = help.help_message
        result_string = embed_txt_message(result_string, color=discord.Color.purple())
        result_string.set_thumbnail(url=constant.TI_LOGO_URL)
        result_string.set_author(name='TI9 COMMANDS')
        result_string = add_footer_requested_by_username(result_string, message)
        await message.channel.send(embed=result_string)
    return True, command_called


async def cmd_broadcast(message, message_string):
    async with message.channel.typing():
        message_split = message_string.split()
        if len(message_split) > 1:
            client_id = message_split[1]
            if str(client_id) == str(DISCORD_CLIENT_ID):
                message = " ".join(message_split[2:])
                await broadcast_message(message)


async def cmd_exit(message, message_string):
    message_split = message_string.split()
    if len(message_split) > 1:
        client_id = message_split[1]
        if str(client_id) == str(DISCORD_CLIENT_ID):
            await message.channel.send(f'Exiting client: {client_id}')
            sys.exit(0)


async def cmd_tail(message, message_string, n=5):
    try:
        n = int(message_string.split()[1])
    except Exception:
        pass
    tail_log = get_command_log_tail(n)
    tail_log = embed_txt_message(tail_log, color=discord.Color.purple())
    tail_log.set_author(name='Command Tail Log')
    tail_log = add_footer_requested_by_username(tail_log, message)
    await message.channel.send(embed=tail_log)


async def get_team(message, message_string, message_word_length):
    command_called = '!team'
    if message_word_length == 2 and ('help' == message_string.split()[1] or 'helps' == message_string.split()[1]):
        result_embed = embed_txt_message(TEAM_CMD_EXAMPLE, color=discord.Color.dark_blue())
        result_embed.set_author(name="Team Command Help", icon_url=constant.DV_ICON_URL, url=constant.DV_SITE_TEAM_URL)
        result_embed.set_thumbnail(url=constant.DEFAULT_EMBED_HEADER['icon_url'])
        await message.channel.send(embed=result_embed)
        return False, command_called

    flag, summary, image_path, hero_list = get_team_mate(message_string)
    if not flag:
        msg = embed_txt_message(summary, color=discord.Color.red())
        await message.channel.send(embed=msg)
        return False, command_called
    else:
        desc = f"Next best Team Hero for **{'**, **'.join(hero_list)}** are:"
        title = f"Next best Team Hero:"
        note = 'Still '
        embed = discord.Embed(description=desc, color=discord.Color.blurple())
        embed.set_author(name=title, icon_url=constant.DV_ICON_URL, url=constant.DV_SITE_TEAM_URL)
        image_file = discord.File(image_path, os.path.basename(image_path))
        embed.set_image(url=f"attachment://{image_file.filename}")
        # embed.add_field(name="Update:", value=(note))
        embed = add_footer_requested_by_username(embed, message)
        await message.channel.send(embed=embed, file=image_file)
        return True, command_called

#################################################################################################


# Where the commands are called
@client.event
async def on_message(message):
    is_command_called = True
    command_called = ""
    message_string = message.content
    message_string = message_string.lower().strip()
    message_word_length = len(message_string.split())
    user_discord_id = message.author.id
    user_discord_name = message.author.name
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")

    # Ignore all message passed by the our bot
    if client.user == message.author:
        is_command_called = False

    elif user_discord_id in [612215331334782990, 612284442131824640]:
        return

    # Ignore if message is from another Bot
    elif message.author.bot:
        is_command_called = False

    elif '!help' == message_string or '--help' == message_string or '!command' in message_string:
        flag, command_called = await cmd_help(message)

    elif ('!top_game' in message_string or '!top game' in message_string) and \
            message_word_length < MAX_COMMAND_WORD_LENGTH:
        flag, command_called = await cmd_top_game(message)

    elif '!profile' in message_string and message_word_length < MAX_COMMAND_WORD_LENGTH:
        flag, command_called = await cmd_profile(message, message_string, message_word_length, user_discord_id)

    elif '!save' in message_string.split()[0]:
        await cmd_save(message, message_string, message_word_length, user_discord_id, user_discord_name)

    elif "!trend" in message_string and message_word_length < (MAX_COMMAND_WORD_LENGTH - 2):
        flag, command_called = await cmd_trend(message)

    elif ("!counter" in message_string or "!bad" in message_string) and message_word_length < MAX_COMMAND_WORD_LENGTH:
        flag, command_called = await cmd_counter(message, message_string)

    elif "!good" in message_string and message_word_length < MAX_COMMAND_WORD_LENGTH:
        flag, command_called = await cmd_good(message, message_string)

    elif ("!skill" in message_string or "!talent" in message_string) \
            and message_word_length < MAX_COMMAND_WORD_LENGTH:
        flag, command_called = await cmd_skill(message, message_string)

    elif "!item" in message_string and message_word_length < MAX_COMMAND_WORD_LENGTH:
        flag, command_called = await cmd_item(message, message_string)

    elif "!twitch" in message_string and message_word_length < MAX_COMMAND_WORD_LENGTH:
        flag, command_called = await cmd_twitch(message, message_string)

    elif "!reddit" in message_string and message_word_length < MAX_COMMAND_WORD_LENGTH:
        flag, command_called = await cmd_reddit(message, message_string)

    elif "!pro" in message_string and message_word_length < MAX_COMMAND_WORD_LENGTH:
        flag, command_called = await cmd_protracker(message, message_string)

    elif "!ti" in message_string:
        flag, command_called = await cmd_ti(message, message_string)

    elif "!update" in message_string and message_word_length < 2:
        await message.channel.send(LAST_UPDATE)

    # elif "!team" in message_string and message_word_length < MAX_COMMAND_WORD_LENGTH:
    #     flag, command_called = await get_team(message, message_string, message_word_length)

    # Admin privilege
    elif "!exit" in message_string and str(message.author) == ADMIN_ID:
        await cmd_exit(message, message_string)

    elif "!broadcast" in message_string and str(message.author) == ADMIN_ID:
        await cmd_broadcast(message, message_string)

    elif "!tail" in message_string and str(message.author) == ADMIN_ID:
        is_command_called = False
        await cmd_tail(message, message_string)

    # Message user
    elif f"{DISCORD_CLIENT_ID}" in message_string:
        await message.channel.send(f"Hello {message.author.name}"
                                   f" Please type    `!help`  or `!command`  for more options")

    else:
        is_command_called = False

    if is_command_called:
        save_command_logs(message, command_called)


client.run(DISCORD_TOKEN)


