import discord
from discord.ext import commands
import os
import random
from bota.guild_process.guild_main import GuildCaller
from bota.constant import DEFAULT_PREFIX

import bota.logs_process.log_utils
from bota.constant import MAX_COMMAND_WORD_LENGTH
from bota.help import get_help, PROFILE_HELP_STRING, get_guild_commands, pretty_guild_settings
from bota.private_constant import DISCORD_TOKEN, DISCORD_CLIENT_ID, ADMIN_ID
from bota.applications.top_games import get_top_games
from bota.web_scrap.scrap import get_current_trend, get_counter_hero, get_good_against, get_reddit, save_id_in_db
from bota.web_scrap.scrap import get_skill_build, get_item_build, get_profile_from_db, get_protracker_hero
from bota.web_scrap.twitch_process import get_dota2_top_stream
from bota.web_scrap.TI import group_stage, help, stats, matches
from bota.web_scrap.dotavoyance.getter import get_team_mate
from bota.logs_process import log_caller
from discord.utils import find
from discord import File
from bota import constant
# from bota.web_scrap.aghanim_process import Agha
from bota.utility.main_utils import prefix_validation_correct, add_footer_requested_by_username, \
    embed_txt_message, get_infos_from_msg

guild_caller = GuildCaller()


def is_channel_block(ctx):
    guild_id = ctx.message.guild.id
    channel_name = str(ctx.channel)
    block_channel_names = guild_caller.get_block_channel_names(guild_id)
    if channel_name in block_channel_names:
        return True
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


class Bota(commands.AutoShardedBot):
    async def get_context(self, message, *, cls=MyContext):
        # when you override this method, you pass your new Context
        # subclass to the super() method, which tells the bot to
        # use the new MyContext class

        return await super().get_context(message, cls=cls)


bot = Bota(command_prefix=determine_prefix)


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
    owner_id = ctx.message.author.guild.owner_id
    author_id = ctx.message.author.id
    guild_id = ctx.message.author.guild.id
    all_channels = [x.name for x in ctx.guild.text_channels]
    messages_split = ctx.message.content.lower().split()
    length = len(messages_split)
    if length == 1:
        guild_commands = get_guild_commands()
        await ctx.send(embed=guild_commands)
    else:
        if owner_id != author_id:
            embed = discord.Embed(description=f"Sorry! Only server owner can make changes",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)

        elif 'setting' in messages_split[1] and length == 2:
            settings = guild_caller.get_guild_settings(guild_id)
            settings_dict = {'Prefix': settings[0], 'Blocked Channels': ", ".join(settings[1])}
            embed = pretty_guild_settings(settings_dict)
            await ctx.send(embed=embed)

        elif messages_split[1] == 'prefix' and length == 3:
            prefix = messages_split[2].strip()
            if not prefix_validation_correct(prefix):
                embed = discord.Embed(description=f"Sorry! prefix should only be a single character: eg: !guild prefix #",
                                      color=discord.Color.red())
                await ctx.send(embed=embed)
            guild_caller.update_prefix(guild_id, prefix)
            embed = discord.Embed(description=f"Success! Prefix updated to: {prefix} ", color=discord.Color.green())
            await ctx.send(embed=embed)

        elif messages_split[1] == 'block' and length == 3:
            channel_name = messages_split[2].strip()
            if channel_name not in all_channels:
                embed = discord.Embed(
                    description=f"No channel name {channel_name} found. All channel names: {all_channels}",
                    color=discord.Color.red())
                await ctx.send(embed=embed)
            guild_caller.add_channel_to_blocklist(guild_id, channel_name)
            embed = discord.Embed(description=f"Success! Channel blocked: {channel_name} ", color=discord.Color.green())
            await ctx.send(embed=embed)

        elif messages_split[1] == 'unblock' and length == 3:
            channel_name = messages_split[2].strip()
            guild_caller.delete_channel_from_blocklist(guild_id, channel_name)
            embed = discord.Embed(description=f"Success! Channel unblocked: {channel_name} ", color=discord.Color.green())
            await ctx.send(embed=embed)


@bot.command(aliases=['command', 'commands', 'cmds'])
async def cmd(ctx):
    """ Gets command list """
    if is_channel_block(ctx):
        return
    help_string_embed_msg = get_help()
    await ctx.send(embed=help_string_embed_msg)


@bot.command(aliases=['topgame', 'top game'])
async def top_game(ctx):
    """Gets Top current live games with Average MMR"""
    if is_channel_block(ctx):
        return
    async with ctx.typing():
        image_path = get_top_games()
        msg = "Top Live Games: Dota2API"
        embed = discord.Embed(color=discord.Color.green())
        embed.title = msg
        image_file = discord.File(image_path, os.path.basename(image_path))
        embed.add_field(name="Source:", value=('[Dota2API](https://demodota2api.readthedocs.io/en/latest/#)'))
        embed.set_image(url=f"attachment://{image_file.filename}")
        embed = add_footer_requested_by_username(embed, ctx.message)
        await ctx.send(embed=embed, file=image_file)
    pass


@bot.command(aliases=['profiles'])
async def profile(ctx):
    """Gets your Profile stats"""
    if is_channel_block(ctx):
        return
    message_string, message_word_length, user_discord_id, user_discord_name = get_infos_from_msg(ctx)
    if message_word_length == 2 and ('help' == message_string.split()[1] or 'helps' == message_string.split()[1]):
        result_embed = embed_txt_message(PROFILE_HELP_STRING, color=discord.Color.dark_blue())
        result_embed.set_author(name="Profile Command Help")
        result_embed.set_thumbnail(url=constant.DEFAULT_EMBED_HEADER['icon_url'])
        await ctx.send(embed=result_embed)

    async with ctx.typing():
        try:
            flag, mode, steam_id, alias_name, result, medal_url, dp_url = get_profile_from_db(user_discord_id, message_string)
        except:
            msg = 'Could not fetch your profile. Please make sure your profile is public'
            msg = embed_txt_message(msg, color=discord.Color.red())
            await ctx.send(embed=msg)

    result_embed = embed_txt_message(result, color=discord.Color.green())
    result_embed.set_author(name=f"SteamID: {steam_id}", url=f'{constant.PLAYER_URL_BASE}{steam_id}',
                            icon_url=dp_url)
    result_embed.set_thumbnail(url=medal_url)
    if not flag:
        if mode == 1:
            msg = f'<@{user_discord_id}> Please save your Steam ID to get your profile, To save your profile:' \
                  f' **`!save SteamID`** eg: **`!save 311360822`**\nPlease type  **`!profile help`**  for more help'
            msg = embed_txt_message(msg, color=discord.Color.red())
            await ctx.send(embed=msg)
        elif mode == 2:
            msg = f'<@{user_discord_id}> Could not find any profile under the Steam ID:    **{steam_id}**\n' \
                  f'Please type  **`!profile help`**  for more help'
            msg = embed_txt_message(msg, color=discord.Color.red())
            await ctx.send(embed=msg)
        else:
            msg = f'<@{user_discord_id}> Could not find User:   **{alias_name}**,  You can save a username by eg: ' \
                  f' **`!save {alias_name} SteamID`** \nPlease type  **`!profile help`**  for more help'
            msg = embed_txt_message(msg, color=discord.Color.red())
            await ctx.send(embed=msg)
    else:
        result_embed = add_footer_requested_by_username(result_embed, ctx.message)
        await ctx.send(embed=result_embed)


@bot.command(aliases=['saves'])
async def save(ctx):
    if is_channel_block(ctx):
        return

    message_string, message_word_length, user_discord_id, user_discord_name = get_infos_from_msg(ctx)
    if message_word_length == 2 and ('help' == message_string.split()[1] or 'helps' == message_string.split()[1]):
        result_embed = embed_txt_message(PROFILE_HELP_STRING, color=discord.Color.red())
        result_embed.set_author(name="Save Command Help")
        result_embed.set_thumbnail(url=constant.DEFAULT_EMBED_HEADER['icon_url'])
        await ctx.send(embed=result_embed)
        return
    async with ctx.typing():
        flag, summary = save_id_in_db(user_discord_id, user_discord_name, message_string)
    if not flag:
        summary = embed_txt_message(summary, color=discord.Color.red())
    else:
        summary = embed_txt_message(summary, color=discord.Color.green())
    summary = add_footer_requested_by_username(summary, ctx.message)
    await ctx.send(embed=summary)


env_var = os.environ
DISCORD_TOKEN = env_var.get('DISCORD_TOKEN')
bot.run(DISCORD_TOKEN)


