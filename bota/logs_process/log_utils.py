import os
import discord
from bota import constant
from datetime import datetime


class LogBackup:
    def __init__(self):
        self.logs = []
        self.last_added_time = ''
        self.last_cleared_time = ''
        self.failed_reason = ''

    def append_log(self, log, reason):
        self.logs.append(log)
        self.last_added_time = str(datetime.now())
        self.failed_reason = reason

    def get_failed_logs(self):
        self.last_cleared_time = str(datetime.now())
        return self.logs

    def clear_failed_logs(self):
        self.logs = []
        self.failed_reason = ''

    def is_fail_logs_in_memory(self):
        if len(self.logs) > 0:
            return True
        return False

    def fail_logs_info(self):
        print(self.logs)
        info = {'length': len(self.logs), 'last_updated_time': self.last_added_time,
                'last_cleared_time': self.last_cleared_time, 'failed_reason': self.failed_reason}
        return info


def embed_discord(title, summary, image_path=None, is_type='dictionary', color=discord.Color.blurple()):
    if is_type == 'dictionary':
        stat_week_text = []
        embed = discord.Embed(color=color, title=title)
        embed.set_author(name=constant.DEFAULT_EMBED_HEADER['name'],
                         icon_url=constant.DEFAULT_EMBED_HEADER['icon_url'],
                         url=constant.DEFAULT_EMBED_HEADER['url'])
        for key, value in summary.items():
            stat_week_text.append(f"**{key}**: {value}")
            embed.add_field(name=key, value=value)
        return embed, ''

    elif is_type == 'image':
        embed = discord.Embed(description=summary, color=discord.Color.blurple(), title=title)
        embed.set_author(name=constant.DEFAULT_EMBED_HEADER['name'],
                         icon_url=constant.DEFAULT_EMBED_HEADER['icon_url'],
                         url=constant.DEFAULT_EMBED_HEADER['url'])
        image_file = discord.File(image_path, os.path.basename(image_path))
        embed.set_image(url=f"attachment://{image_file.filename}")
        return embed, image_file


def is_command_from_channel(message):
    channel = str(message.channel)
    if 'Direct Message' in channel:
        return False
    return True


def extract_info(message, command_called):
    guild_id = ""
    guild_name = ""
    guild_member_count = ""
    channel_name = ""
    channel_nsfw = ""
    author = message.author
    author_id = message.author.id
    content = message.content
    command_channel_flag = is_command_from_channel(message)
    if command_channel_flag:
        guild_id = message.guild.id
        guild_name = message.guild.name
        guild_member_count = message.guild.member_count
        channel_name = message.channel.name
        channel_nsfw = message.channel.nsfw

    info = [str(author), str(author_id), str(command_channel_flag), str(guild_id), str(guild_name), channel_name,
            str(guild_member_count), str(command_called), str(channel_nsfw), content]

    log_text = ",".join(info)
    return log_text