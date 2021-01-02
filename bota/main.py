import discord
from discord.ext import commands
import os
import random
import sys
from bota.guild_process.guild_main import GuildCaller
from bota.constant import DEFAULT_PREFIX

import bota.logs_process.log_utils
# from bota.constant import MAX_COMMAND_WORD_LENGTH
from bota.help import get_help, PROFILE_HELP_STRING, get_guild_commands, pretty_guild_settings, COUNTER_EXAMPLE, \
    UPDATE_BLOCK, GOOD_EXAMPLE, REDDIT_CMD_EXAMPLE, LAST_UPDATE, get_admin_commands
from bota.private_constant import DISCORD_TOKEN, DISCORD_CLIENT_ID, ADMIN_ID
from bota.applications.top_games import get_top_games
from bota.web_scrap.scrap import get_current_trend, get_counter_hero, get_good_against, get_reddit, save_id_in_db
from bota.web_scrap.scrap import get_skill_build, get_item_build, get_profile_from_db, get_protracker_hero, get_meta
from bota.web_scrap.twitch_process import get_dota2_top_stream
from bota.web_scrap.TI import group_stage, help, stats, matches
# from bota.web_scrap.dotavoyance.getter import get_team_mate
from bota.logs_process import log_caller
from discord.utils import find
from discord import File
from bota import constant
from bota.web_scrap.aghanim_process import Agha
from bota.utility.main_utils import prefix_validation_correct, add_footer_requested_by_username, \
    embed_txt_message, get_infos_from_msg

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', help='test mode', default=False)
args = vars(parser.parse_args())
TEST_MODE = args['test']

guild_caller = GuildCaller()
GUILDS = []
AGHA = Agha()
GUILDS = []
UPDATE_BLOCK = UPDATE_BLOCK
CURRENT_PREFIX = DEFAULT_PREFIX


def is_channel_block(ctx):
    try:
        guild_id = ctx.message.guild.id
        channel_name = str(ctx.channel)
        block_channel_names = guild_caller.get_block_channel_names(guild_id)
        if channel_name in block_channel_names:
            return True
        return False
    except:
        return False


async def determine_prefix(bot, message):
    guild = message.guild
    if guild:
        prefix = guild_caller.get_prefix(guild.id, guild.name)
        return prefix
    else:
        return DEFAULT_PREFIX


################## Commands ###############
class MyContext(commands.Context):
    async def tick(self, value):
        emoji = '\N{WHITE HEAVY CHECK MARK}' if value else '\N{CROSS MARK}'
        try:
            # this will react to the command author's message
            await self.message.add_reaction(emoji)
        except discord.HTTPException:
            pass

    async def update_logs(self, message, command_called, is_test=TEST_MODE):
        if is_test:
            return
        log_caller.save_log(message, command_called)
        print(f"{message.author.name}: {message.author}: {message.channel}: {message.content[:100]}")
        log_caller.update_value_to_server()


class Bota(commands.AutoShardedBot):
    async def get_context(self, message, *, cls=MyContext):
        # when you override this method, you pass your new Context
        # subclass to the super() method, which tells the bot to
        # use the new MyContext class
        if f"{DISCORD_CLIENT_ID}" in message.content:
            prefix = await bot.get_prefix(message)
            await message.channel.send(f"Hello **{message.author.name}**. "
                                       f"Please type `{prefix}help`  or `{prefix}command`  for more options")

        return await super().get_context(message, cls=cls)


bot = Bota(command_prefix=determine_prefix)
bot.remove_command(name='help')


## event
@bot.event  # event decorator/wrapper
async def on_ready():
    global GUILDS
    GUILDS = bot.guilds
    await bot.change_presence(activity=discord.Game(name="Dota2 | type '!help'"))
    print(f"Logged in as {bot.user}")


@bot.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general', guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send(f'Hello **{format(guild.name)}**✌✌!\n'
                           f'Type   `!help` or `!command`   to get list of commands to use.')


## commands
@bot.command()
async def guess(ctx, number: int):
    """ Guess a random number from 1 to 6. """
    # explained in a previous example, this gives you
    # a random number from 1-6
    value = random.randint(1, 6)
    # with your new helper function, you can add a
    # green check mark if the guess was correct,
    # or a red cross mark if it wasnt
    await ctx.tick(number == value)


@bot.command()
async def guild(ctx):
    """ Command to manage BOTA in your server."""
    prefix = await bot.get_prefix(ctx.message)
    owner_id = ctx.message.author.guild.owner_id
    author_id = ctx.message.author.id
    guild_id = ctx.message.author.guild.id
    all_channels = [x.name for x in ctx.guild.text_channels]
    messages_split = ctx.message.content.lower().split()
    length = len(messages_split)

    if owner_id != author_id:
        embed = discord.Embed(description=f"Sorry! Only server owner can use **`{prefix}guild`** command",
                              color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    if length == 1:
        guild_commands = get_guild_commands(prefix=prefix)
        await ctx.send(embed=guild_commands)
    else:
        if owner_id != author_id:
            embed = discord.Embed(description=f"Sorry! Only server owner can make changes",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)

        elif 'setting' in messages_split[1] and length == 2:
            settings = guild_caller.get_guild_settings(guild_id)
            blocked_channels = ", ".join(settings[2])
            blocked_channels = blocked_channels if blocked_channels != '' else '-'
            settings_dict = {'Guild Name': settings[0], 'Prefix': settings[1], 'Blocked Channels': blocked_channels}
            # print(settings_dict)
            settings_embed = pretty_guild_settings(settings_dict)
            await ctx.send(embed=settings_embed)
            # await ctx.message.author.send(embed=settings_embed)

        elif messages_split[1] == 'prefix' and length == 3:
            prefix = messages_split[2].strip()
            if not prefix_validation_correct(prefix):
                embed = discord.Embed(
                    description=f"Sorry! prefix should only be a single character: eg: !guild prefix #",
                    color=discord.Color.red())
                await ctx.send(embed=embed)
                return
            guild_caller.update_prefix(guild_id, prefix)
            settings = guild_caller.get_guild_settings(guild_id)
            blocked_channels = ", ".join(settings[2])
            blocked_channels = blocked_channels if blocked_channels != '' else '-'
            settings_dict = {'Guild Name': settings[0], 'Prefix': settings[1], 'Blocked Channels': blocked_channels}
            head = "**New Guild settings**:\n\n"
            settings_embed = pretty_guild_settings(settings_dict, head=head)
            embed = discord.Embed(description=f"Success. Prefix updated to: **{prefix}** ", color=discord.Color.green())
            await ctx.send(embed=embed)
            await ctx.message.author.send(embed=settings_embed)

        elif messages_split[1] == 'block' and length == 3:
            channel_name = messages_split[2].strip()
            if channel_name not in all_channels:
                embed = discord.Embed(
                    description=f"No channel name **{channel_name}** found. All channel names: **{all_channels}**",
                    color=discord.Color.red())
                await ctx.send(embed=embed)
                return
            guild_caller.add_channel_to_blocklist(guild_id, channel_name)
            settings = guild_caller.get_guild_settings(guild_id)
            blocked_channels = ", ".join(settings[2])
            blocked_channels = blocked_channels if blocked_channels != '' else '-'
            settings_dict = {'Guild Name': settings[0], 'Prefix': settings[1], 'Blocked Channels': blocked_channels}
            head = "**New Guild settings**:\n\n"
            settings_embed = pretty_guild_settings(settings_dict, head=head)
            embed = discord.Embed(description=f"Success. Channel blocked: **{channel_name}** ",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
            await ctx.message.author.send(embed=settings_embed)

        elif messages_split[1] == 'unblock' and length == 3:
            channel_name = messages_split[2].strip()
            guild_caller.delete_channel_from_blocklist(guild_id, channel_name)
            settings = guild_caller.get_guild_settings(guild_id)
            blocked_channels = ", ".join(settings[2])
            blocked_channels = blocked_channels if blocked_channels != '' else '-'
            settings_dict = {'Guild Name': settings[0], 'Prefix': settings[1], 'Blocked Channels': blocked_channels}
            head = "**New Guild settings**:\n\n"
            settings_embed = pretty_guild_settings(settings_dict, head=head)
            embed = discord.Embed(description=f"Success. Channel unblocked: **{channel_name}** ",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
            await ctx.message.author.send(embed=settings_embed)


@bot.command(aliases=['command', 'commands', 'cmds', 'HELP', 'cmd'])
async def help(ctx):
    """ Gets command list """
    if is_channel_block(ctx):
        return
    prefix = await bot.get_prefix(ctx.message)
    help_string_embed_msg = get_help(prefix)
    await ctx.send(embed=help_string_embed_msg)


@bot.command(aliases=['topgame', 'top game'])
async def top_game(ctx):
    """Gets Top current live games with Average MMR"""
    if is_channel_block(ctx):
        return
    prefix = await bot.get_prefix(ctx.message)
    async with ctx.typing():
        image_path = get_top_games()
        msg = "Top Live Games: Dota2API"
        embed = discord.Embed(color=discord.Color.green())
        embed.title = msg
        image_file = discord.File(image_path, os.path.basename(image_path))
        embed.add_field(name="Source:", value=('[Dota2API](https://demodota2api.readthedocs.io/en/latest/#)'))
        embed.set_image(url=f"attachment://{image_file.filename}")
        embed = add_footer_requested_by_username(embed, ctx.message, prefix=prefix)
        await ctx.send(embed=embed, file=image_file)

    await ctx.update_logs(ctx.message, "!top_game")


@bot.command(aliases=['profiles', 'PROFILE'])
async def profile(ctx):
    """Gets your Profile stats"""
    if is_channel_block(ctx):
        return
    prefix = await bot.get_prefix(ctx.message)
    message_string, message_word_length, user_discord_id, user_discord_name = get_infos_from_msg(ctx)
    if message_word_length == 2 and ('help' == message_string.split()[1] or 'helps' == message_string.split()[1]):
        result_embed = embed_txt_message(PROFILE_HELP_STRING.replace('!', prefix), color=discord.Color.dark_blue())
        result_embed.set_author(name="Profile Command Help")
        result_embed.set_thumbnail(url=constant.DEFAULT_EMBED_HEADER['icon_url'])
        await ctx.send(embed=result_embed)
        return

    async with ctx.typing():
        try:
            flag, mode, steam_id, alias_name, result, medal_url, dp_url = get_profile_from_db(user_discord_id,
                                                                                              message_string)
        except:
            msg = 'Could not fetch your profile. Please make sure your profile is public'
            msg = embed_txt_message(msg, color=discord.Color.red())
            await ctx.send(embed=msg)
            return

    result_embed = embed_txt_message(result, color=discord.Color.green())
    result_embed.set_author(name=f"SteamID: {steam_id}", url=f'{constant.PLAYER_URL_BASE}{steam_id}',
                            icon_url=dp_url)
    result_embed.set_thumbnail(url=medal_url)
    if not flag:
        if mode == 1:
            msg = f'<@{user_discord_id}> Please save your Steam ID to get your profile, To save your profile:' \
                  f' **`{prefix}save SteamID`** eg: **`{prefix}save 311360822`**\nPlease type  **`{prefix}profile help`**  for more help'
            msg = embed_txt_message(msg, color=discord.Color.red())
            await ctx.send(embed=msg)
        elif mode == 2:
            msg = f'<@{user_discord_id}> Could not find any profile under the Steam ID:    **{steam_id}**\n' \
                  f'Please type  **`{prefix}profile help`**  for more help'
            msg = embed_txt_message(msg, color=discord.Color.red())
            await ctx.send(embed=msg)
        else:
            msg = f'<@{user_discord_id}> Could not find User:   **{alias_name}**,  You can save a username by eg: ' \
                  f' **`{prefix}save {alias_name} SteamID`** \nPlease type  **`{prefix}profile help`**  for more help'
            msg = embed_txt_message(msg, color=discord.Color.red())
            await ctx.send(embed=msg)
    else:
        result_embed = add_footer_requested_by_username(result_embed, ctx.message, prefix=prefix)
        await ctx.send(embed=result_embed)

    await ctx.update_logs(ctx.message, "!profile")


@bot.command(aliases=['saves'])
async def save(ctx):
    if is_channel_block(ctx):
        return
    prefix = await bot.get_prefix(ctx.message)
    message_string, message_word_length, user_discord_id, user_discord_name = get_infos_from_msg(ctx)
    if message_word_length == 2 and ('help' == message_string.split()[1] or 'helps' == message_string.split()[1]):
        result_embed = embed_txt_message(PROFILE_HELP_STRING.replace("!", prefix), color=discord.Color.red())
        result_embed.set_author(name="Save Command Help")
        result_embed.set_thumbnail(url=constant.DEFAULT_EMBED_HEADER['icon_url'])
        await ctx.send(embed=result_embed)
        return
    async with ctx.typing():
        flag, summary = save_id_in_db(user_discord_id, user_discord_name, message_string)
        summary = summary.replace("!", prefix)
    if not flag:
        summary = embed_txt_message(summary, color=discord.Color.red())
    else:
        summary = embed_txt_message(summary, color=discord.Color.green())
    summary = add_footer_requested_by_username(summary, ctx.message, prefix=prefix)
    await ctx.send(embed=summary)


@bot.command(aliases=['trends'])
async def trend(ctx):
    if is_channel_block(ctx):
        return
    prefix = await bot.get_prefix(ctx.message)
    async with ctx.typing():
        image_path = get_current_trend()
        msg = "Current Heroes Trend"
        desc = "Weekly Heroes Trend: Win Rate and Pick Rate"
        embed = discord.Embed(description=desc, color=discord.Color.green())
        embed.title = msg
        image_file = discord.File(image_path, os.path.basename(image_path))
        embed.add_field(name="Source:", value=('[DotaBuff](https://www.dotabuff.com/heroes/trends)'))
        embed.set_image(url=f"attachment://{image_file.filename}")
        embed = add_footer_requested_by_username(embed, ctx.message, prefix=prefix)
        await ctx.send(embed=embed, file=image_file)
    await ctx.update_logs(ctx.message, "!trend")


@bot.command(aliases=['META', 'metas'])
async def meta(ctx):
    if is_channel_block(ctx):
        return
    prefix = await bot.get_prefix(ctx.message)
    async with ctx.typing():
        image_path = get_meta()
        msg = "Heroes Meta Statistics"
        desc = "This month Hero Meta with MMR Brackets"
        embed = discord.Embed(description=desc, color=discord.Color.green())
        embed.title = msg
        image_file = discord.File(image_path, os.path.basename(image_path))
        embed.add_field(name="Source:", value=(f'[DotaBuff]({constant.META_URL})'))
        embed.set_image(url=f"attachment://{image_file.filename}")
        embed = add_footer_requested_by_username(embed, ctx.message, prefix=prefix)
        await ctx.send(embed=embed, file=image_file)
    await ctx.update_logs(ctx.message, "!trend")


@bot.command(aliases=['counters', 'bad', 'COUNTER', 'COUNTERS', 'BAD'])
async def counter(ctx):
    if is_channel_block(ctx):
        return
    prefix = await bot.get_prefix(ctx.message)
    message_string, message_word_length, user_discord_id, user_discord_name = get_infos_from_msg(ctx)
    if message_word_length == 2 and ('help' == message_string.split()[1] or 'helps' == message_string.split()[1]):
        result_embed = embed_txt_message(COUNTER_EXAMPLE.replace("!", prefix), color=discord.Color.dark_red())
        result_embed.set_author(name="Counter Command Help")
        result_embed.set_thumbnail(url=constant.DEFAULT_EMBED_HEADER['icon_url'])
        await ctx.send(embed=result_embed)
        return

    async with ctx.typing():
        note = UPDATE_BLOCK.replace("!", prefix)
        found, hero_name, image_path = get_counter_hero(message_string)
        if not found:
            if hero_name != '':
                msg = f"Did you mean  **{hero_name.replace('-', ' ')}**, Try again with correct name"
                msg = embed_txt_message(msg, color=discord.Color.red())
                await ctx.send(embed=msg)
            else:
                msg = f"Could not find hero, Please make sure the hero name is correct.\nType **`!counter help`**  for more help"
                msg = embed_txt_message(msg, color=discord.Color.red())
                await ctx.send(embed=msg)
            return
        else:
            desc = f'**Source**: [DotaBuff](https://www.dotabuff.com/heroes/{hero_name}/counters)'
            title = f"{hero_name.upper()} is BAD against:"
            embed = discord.Embed(description=desc, color=discord.Color.red(), title=title)
            image_file = discord.File(image_path, os.path.basename(image_path))
            embed.set_image(url=f"attachment://{image_file.filename}")
            embed.set_thumbnail(url=f'{constant.CHARACTER_ICONS_URL}{hero_name}.png')
            embed.add_field(name="Update:", value=(note))
            embed = add_footer_requested_by_username(embed, ctx.message, prefix=prefix)
            await ctx.send(embed=embed, file=image_file)
            await ctx.update_logs(ctx.message, "!counter")
            return


@bot.command(aliases=['goods', 'GOOD', 'GOODS'])
async def good(ctx):
    if is_channel_block(ctx):
        return
    prefix = await bot.get_prefix(ctx.message)
    message_string, message_word_length, user_discord_id, user_discord_name = get_infos_from_msg(ctx)

    if message_word_length == 2 and ('help' == message_string.split()[1] or 'helps' == message_string.split()[1]):
        result_embed = embed_txt_message(GOOD_EXAMPLE.replace("!", prefix), color=discord.Color.dark_red())
        result_embed.set_author(name="Good Command Help")
        result_embed.set_thumbnail(url=constant.DEFAULT_EMBED_HEADER['icon_url'])
        await ctx.send(embed=result_embed)
        return
    async with ctx.typing():
        note = UPDATE_BLOCK.replace("!", prefix)
        found, hero_name, image_path = get_good_against(message_string)
        if not found:
            if hero_name != '':
                msg = f"Did you mean  **{hero_name.replace('-', ' ')}**, Try again with correct name "
                msg = embed_txt_message(msg, color=discord.Color.red())
                await ctx.send(embed=msg)
            else:
                msg = f"Could not find hero, Please make sure the hero name is correct"
                msg = embed_txt_message(msg, color=discord.Color.red())
                await ctx.send(embed=msg)
            return
        else:
            desc = f'**Source**: [DotaBuff](https://www.dotabuff.com/heroes/{hero_name}/counters)'
            title = f"{hero_name.upper()} is GOOD against:"
            embed = discord.Embed(description=desc, color=discord.Color.green(), title=title)
            image_file = discord.File(image_path, os.path.basename(image_path))
            embed.set_image(url=f"attachment://{image_file.filename}")
            embed.add_field(name="Update:", value=(note))
            embed.set_thumbnail(url=f'{constant.CHARACTER_ICONS_URL}{hero_name}.png')
            embed = add_footer_requested_by_username(embed, ctx.message, prefix=prefix)
            await ctx.send(embed=embed, file=image_file)
            await ctx.update_logs(ctx.message, "!good")
            return


@bot.command(aliases=['skills', 'SKILL', 'SKILLS', 'talent', 'talents', 'TALENT'])
async def skill(ctx):
    if is_channel_block(ctx):
        return
    prefix = await bot.get_prefix(ctx.message)
    message_string, message_word_length, user_discord_id, user_discord_name = get_infos_from_msg(ctx)

    async with ctx.typing():
        note = UPDATE_BLOCK.replace("!", prefix)
        found, hero_name, image_path = get_skill_build(message_string)
        if not found:
            if hero_name != '':
                msg = f"Did you mean  **{hero_name.replace('-', ' ')}**, Try again with correct name"
                msg = embed_txt_message(msg, color=discord.Color.red())
                await ctx.send(embed=msg)
            else:
                msg = f"Could not find hero, Please make sure the hero name is correct"
                msg = embed_txt_message(msg, color=discord.Color.red())
                await ctx.send(embed=msg)
            return
        else:
            desc = f'**{hero_name.upper()}** most popular Skill/Talent build, **Source**: [DotaBuff](https://www.dotabuff.com/heroes/{hero_name})'
            title = f"{hero_name.upper()} Skill/Talent buildt:"
            embed = discord.Embed(description=desc, color=discord.Color.blurple(), title=title)
            image_file = discord.File(image_path, os.path.basename(image_path))
            embed.set_image(url=f"attachment://{image_file.filename}")
            embed.add_field(name="Update:", value=(note))
            embed.set_thumbnail(url=f'{constant.CHARACTER_ICONS_URL}{hero_name}.png')
            embed = add_footer_requested_by_username(embed, ctx.message, prefix=prefix)
            await ctx.send(embed=embed, file=image_file)
            await ctx.update_logs(ctx.message, "!skill")
            return


@bot.command(aliases=['items', 'ITEM', 'ITEMS'])
async def item(ctx):
    if is_channel_block(ctx):
        return
    prefix = await bot.get_prefix(ctx.message)
    message_string, message_word_length, user_discord_id, user_discord_name = get_infos_from_msg(ctx)

    async with ctx.typing():
        note = UPDATE_BLOCK.replace("!", prefix)
        found, hero_name, image_path = get_item_build(message_string)
        if not found:
            if hero_name != '':
                msg = f"Did you mean  **{hero_name.replace('-', ' ')}**, Try again with correct name"
                msg = embed_txt_message(msg, color=discord.Color.red())
                await ctx.send(embed=msg)
            else:
                msg = f"Could not find hero, Please make sure the hero name is correct\nType **`!good help`**  for more help"
                msg = embed_txt_message(msg, color=discord.Color.red())
                await ctx.send(embed=msg)
            return
        else:
            desc = f'**{hero_name.upper()}** recent Item build by **Top Rank Players**:, [DotaBuff](https://www.dotabuff.com/heroes/{hero_name}/guides)'
            title = f"{hero_name.upper()} Item Build:"
            embed = discord.Embed(description=desc, color=discord.Color.blurple(), title=title)
            image_file = discord.File(image_path, os.path.basename(image_path))
            embed.set_image(url=f"attachment://{image_file.filename}")
            embed.add_field(name="Update:", value=(note))
            embed.set_thumbnail(url=f'{constant.CHARACTER_ICONS_URL}{hero_name}.png')
            embed = add_footer_requested_by_username(embed, ctx.message, prefix=prefix)
            await ctx.send(embed=embed, file=image_file)
            await ctx.update_logs(ctx.message, "!item")
            return


@bot.command(aliases=['twitchs', 'TWITCH'])
async def twitch(ctx):
    if is_channel_block(ctx):
        return
    message_string, message_word_length, user_discord_id, user_discord_name = get_infos_from_msg(ctx)
    prefix = await bot.get_prefix(ctx.message)
    async with ctx.typing():
        language = None if len(message_string.split()) <= 1 else message_string.split()[1]
        result = get_dota2_top_stream(language)
    embed_msg = embed_txt_message(result)
    embed_msg = add_footer_requested_by_username(embed_msg, ctx.message, prefix=prefix)
    await ctx.send(embed=embed_msg)
    await ctx.update_logs(ctx.message, "!twitch")
    return


@bot.command(aliases=['reddits', 'REDDIT', 'redit'])
async def reddit(ctx):
    if is_channel_block(ctx):
        return
    prefix = await bot.get_prefix(ctx.message)
    message_string, message_word_length, user_discord_id, user_discord_name = get_infos_from_msg(ctx)

    if message_word_length == 2 and ('help' == message_string.split()[1] or 'helps' == message_string.split()[1]):
        result_embed = embed_txt_message(REDDIT_CMD_EXAMPLE.replace("!", prefix), color=discord.Color.dark_red())
        result_embed.set_author(name="Profile Command Help")
        result_embed.set_thumbnail(url=constant.DEFAULT_EMBED_HEADER['icon_url'])
        await ctx.send(embed=result_embed)
        return

    async with ctx.typing():
        result_list, mode = get_reddit(message_string)
    await ctx.send(f"**REDDIT**  SortBy: **{mode.upper()}**, Source: Reddit")
    for result in result_list:
        await ctx.send(f'{result}')
    await ctx.update_logs(ctx.message, "!reddit")
    return


@bot.command(aliases=['tis', 'TI'])
async def ti(ctx):
    if is_channel_block(ctx):
        return
    prefix = await bot.get_prefix(ctx.message)
    message_string, message_word_length, user_discord_id, user_discord_name = get_infos_from_msg(ctx)
    message_split = message_string.split()
    if len(message_split) > 1 and 'group' in message_split[1]:
        async with ctx.typing():
            command_called = f'{prefix}ti group'
            result_string = group_stage.get_group_stage()
            result_string = f'Type **`{prefix}ti main`** to get TI Main Stage bracket and schedule\n' + result_string
        result_string = embed_txt_message(result_string, color=discord.Color.purple())
        result_string.set_thumbnail(url=constant.TI_LOGO_URL)
        result_string.set_author(name='TI9 GROUP STAGE')
        result_string = add_footer_requested_by_username(result_string, ctx.message, prefix=prefix)
        await ctx.send(embed=result_string)

    elif len(message_split) > 1 and 'stat' in message_split[1]:
        async with ctx.typing():
            command_called = f'{prefix}ti stat'
            result_string = stats.get_all_stats()
        result_string = embed_txt_message(result_string, color=discord.Color.purple())
        result_string.set_thumbnail(url=constant.TI_LOGO_URL)
        result_string.set_author(name='TI9 Hero Stats')
        result_string = add_footer_requested_by_username(result_string, ctx.message, prefix=prefix)
        await ctx.send(embed=result_string)

    elif len(message_split) > 1 and 'match' in message_split[1]:
        result_string = f"Could not fetch Upcoming matches\nType  **`{prefix}ti main`** to get TI Main Stage bracket and schedule"
        async with ctx.typing():
            try:
                command_called = f'{prefix}ti match'
                result_string = matches.get_all_matches()
            except Exception:
                pass
        await ctx.send(result_string)

    elif len(message_split) > 1 and 'main' in message_split[1]:
        async with ctx.typing():
            command_called = f'{prefix}ti main'
            result_string = group_stage.get_main_stage()
        result_string = embed_txt_message(result_string, color=discord.Color.purple())
        result_string.set_thumbnail(url=constant.TI_LOGO_URL)
        result_string.set_author(name='TI9 Main Stage Schedule')
        result_string = add_footer_requested_by_username(result_string, ctx.message, prefix=prefix)
        await ctx.send(embed=result_string)

    else:
        result_string = help.help_message
        result_string = embed_txt_message(result_string, color=discord.Color.purple())
        result_string.set_thumbnail(url=constant.TI_LOGO_URL)
        result_string.set_author(name='TI9 COMMANDS')
        result_string = add_footer_requested_by_username(result_string, ctx.message, prefix=prefix)
        await ctx.send(embed=result_string)
    await ctx.update_logs(ctx.message, command_called)
    return


@bot.command()
async def update(ctx):
    if is_channel_block(ctx):
        return
    await ctx.send(LAST_UPDATE)


@bot.command(aliases=['aghanim', 'AGHANIM', 'AGHA', 'scepter', 'SCEPTER'])
async def agha(ctx):
    if is_channel_block(ctx):
        return
    message_string, message_word_length, user_discord_id, user_discord_name = get_infos_from_msg(ctx)
    command_called = '!agha'
    hero_name = message_string.split()[1:]
    hero_name = " ".join(hero_name)
    flag, hero_name, embed = AGHA.get_agha_info(hero_name)

    if not flag:
        if hero_name != '':
            embed = discord.Embed(
                description=f"Did you mean  **{hero_name.replace('-', ' ')}**, Try again with correct name",
                color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f"Could not find hero, Please make sure the hero name is correct",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
        return False, command_called

    else:
        await ctx.send(embed=embed)
        await ctx.update_logs(ctx.message, '!agha')
    return True, command_called


########## Bota owner commands

@bot.command(aliases=['ADMIN'])
async def admin(ctx):
    user_id = str(ctx.message.author).strip()
    if user_id != ADMIN_ID:
        return
    prefix = await bot.get_prefix(ctx.message)
    admin_commands = get_admin_commands(prefix=prefix)
    await ctx.send(embed=admin_commands)


@bot.command(aliases=['STAT', 'stats'])
async def stat(ctx):
    user_id = str(ctx.message.author).strip()
    if user_id != ADMIN_ID:
        return

    message_string, message_word_length, user_discord_id, user_discord_name = get_infos_from_msg(ctx)
    message_splitted = message_string.split()

    show_all = False
    if message_word_length > 1 and 'all' in message_splitted[1] and message_word_length == 2:
        show_all = True

    if message_word_length == 1 or show_all:
        text_dict = log_caller.get_stat_all_time()  # logstat.all_time()
        title = "Weekly All Time Stats"
        embed, _ = bota.logs_process.log_utils.embed_discord(title,
                                                             text_dict)  # logstat.embed_discord(title, text_dict)
        await ctx.send(embed=embed)
        if not show_all:
            return

    if ('user' in message_splitted[1] or 'new' in message_splitted[1] or 'server' in message_splitted[1]) or show_all:
        n = 21
        if message_word_length == 3:
            n = int(message_splitted[2])
        img_path, summary = log_caller.get_stat_new_user_server(n)  # logstat.get_new_user_and_server(n=n)
        title = 'New User and Server'
        embed, image_embed = bota.logs_process.log_utils.embed_discord(title, summary, image_path=img_path,
                                                                       is_type='image')
        # logstat.embed_discord(title, summary, image_path=img_path, is_type='image')
        await ctx.send(embed=embed, file=image_embed)
        if not show_all:
            return

    if 'command' in message_splitted[1] or 'cmd' in message_splitted[1] or show_all:
        n = 14
        if message_word_length == 3:
            n = int(message_splitted[2])
        img_path_1, summary_1 = log_caller.get_stat_commands(n)  # logstat.get_commands_stats(n=14)
        img_path_2, summary_2 = log_caller.get_stat_calls(n)  # logstat.get_command_calls(n=n)
        title_1 = "All Commands Stats"
        title_2 = "Command Calls Stats"
        embed_1, image_1_embed = bota.logs_process.log_utils.embed_discord(title_1, summary_1, image_path=img_path_1,
                                                                           is_type='image')
        embed_2, image_2_embed = bota.logs_process.log_utils.embed_discord(title_2, summary_2, image_path=img_path_2,
                                                                           is_type='image')
        await ctx.send(embed=embed_2, file=image_2_embed)
        await ctx.send(embed=embed_1, file=image_1_embed)
        if not show_all:
            return

    if 'update' in message_splitted[1]:
        flag = log_caller.stats_update()
        log_caller.update_value_to_server(force_update=True)
        if flag:
            embed = discord.Embed(title="Updated The Log DF", color=discord.Color.green())
        else:
            embed = discord.Embed(title="Could not find the Log file", color=discord.Color.red())
        await ctx.send(embed=embed)


@bot.command(aliases=['EXIT'])
async def exit(ctx):
    user_id = str(ctx.message.author).strip()
    if user_id != ADMIN_ID:
        return

    message_string, message_word_length, user_discord_id, user_discord_name = get_infos_from_msg(ctx)
    message_split = message_string.split()
    if len(message_split) > 1:
        client_id = message_split[1]
        if str(client_id) == str(DISCORD_CLIENT_ID):
            await ctx.send(f'Exiting client: {client_id}')
            sys.exit(0)


@bot.command()
async def broadcast(ctx):
    user_id = str(ctx.message.author).strip()
    if user_id != ADMIN_ID:
        return
    message_string, message_word_length, user_discord_id, user_discord_name = get_infos_from_msg(ctx)
    global GUILDS
    async with ctx.typing():
        message_split = message_string.split()
        if len(message_split) > 1:
            client_id = message_split[1]
            if str(client_id) == str(DISCORD_CLIENT_ID):
                message = " ".join(message_split[2:])
                for g in GUILDS:
                    await g.text_channels[0].send(message)


@bot.command(aliases=['tails', 'TAIL'])
async def tail(ctx):
    user_id = str(ctx.message.author).strip()
    if user_id != ADMIN_ID:
        return
    prefix = await bot.get_prefix(ctx.message)
    message_string, message_word_length, user_discord_id, user_discord_name = get_infos_from_msg(ctx)
    n = 5
    try:
        n = int(message_string.split()[1])
    except Exception:
        pass
    tail_log = log_caller.get_command_log_tail(n)
    tail_log = embed_txt_message(tail_log, color=discord.Color.purple())
    tail_log.set_author(name='Command Tail Log')
    tail_log = add_footer_requested_by_username(tail_log, ctx.message, prefix=prefix)
    await ctx.send(embed=tail_log)


@bot.command(aliases=['NGUILD'])
async def nguild(ctx):
    prefix = await bot.get_prefix(ctx.message)
    user_id = str(ctx.message.author).strip()
    if user_id != ADMIN_ID:
        return
    nguilds = len(list(bot.guilds))
    await ctx.send(f"{nguilds}")


@bot.command()
async def loglocal(ctx):
    user_id = str(ctx.message.author).strip()
    if user_id != ADMIN_ID:
        return

    message_string = ctx.message.content
    if 'clear' in message_string:
        log_caller.log_backup.clear_failed_logs()
        await ctx.send("Cleared")
    else:
        info = str(log_caller.log_backup.fail_logs_info())
        await ctx.send(info)


@bot.command()
async def bglog(ctx):
    user_id = str(ctx.message.author).strip()
    if user_id != ADMIN_ID:
        return
    message_string = ctx.message.content
    if "download" in message_string:
        await ctx.send('Background Scrap logs:', file=File(constant.SCRAP_LOG_PATH))

    else:
        with open(constant.SCRAP_LOG_PATH) as f:
            file = f.readlines()
            lines = "Background Scrap logs: \n```cs\n" + "".join(file[-30:]) + "```"
            await ctx.send(lines)


@bot.command(aliases=['restart bota'])
async def restart_bota(ctx):
    user_id = str(ctx.message.author).strip()
    if user_id != ADMIN_ID:
        return
    lines = "Restarting BOTA"
    await ctx.send(lines)
    sys.exit()


@bot.command()
async def updateblock(ctx):
    global UPDATE_BLOCK
    message_string = ctx.message.content
    update_txt = message_string.split()[1:]
    update_txt = " ".join(update_txt)
    UPDATE_BLOCK = update_txt
    await ctx.send('Updated Block message')


# Messager user


env_var = os.environ
bot.run(DISCORD_TOKEN)

