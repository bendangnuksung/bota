import argparse
from bota.private_constant import ADMIN_ID

from datetime import datetime


DEFAULT_LOG_PATH = "bota/data/logs/command_user_log.txt"
DEFAULT_LOG_PATH = "/home/ben/personal/bota/unsaved_logs/command_user_log.txt"


parser = argparse.ArgumentParser(description='Analyse Data from logs')
parser.add_argument('-p','--path', help='Path to log file', default=DEFAULT_LOG_PATH)
args = vars(parser.parse_args())

log_path = args['path']


# Log header
# [str(author), str(author_id), str(command_channel_flag), str(guild_id), str(guild_name), channel_name,
#             str(guild_member_count), str(command_called), str(channel_nsfw), content]
header_commander_arrangement = ["author", "author_id", "command_channel_flag", "guild_id", "guild_name", "channel_name",
                                "guild_member_count", "command_called", "channel_nsfw", "message"]



def analyse_command_logs():
    file = open(log_path, 'r')
    total_personal_calls = 0
    total_guild_calls = 0
    guild_info = {}
    command_called_counter = {}

    for line in file.readlines():
        if 'INFO' not in line:
            continue
        time, logs = line.split('INFO')
        try:
            author, author_id, command_channel_flag, guild_id, guild_name,\
            channel_name, guild_member_count, command_called, nsfw, message = logs.split(',')
        except Exception:
            author, author_id, command_channel_flag, guild_id, guild_name, \
            channel_name, guild_member_count, command_called, nsfw = logs.split(',')[:9]
            message = " ".join(logs.split(',')[9:])


        if command_called not in command_called_counter:
            command_called_counter[command_called] = 1
        else:
            command_called_counter[command_called] += 1


        is_call_from_guild = True if len(guild_id) > 1 else False

        if not is_call_from_guild:
            total_personal_calls += 1
        else:
            total_guild_calls += 1

        if not is_call_from_guild:
            continue

        if guild_id not in guild_info:
            guild_info[guild_id] = {'name': guild_name, 'total_calls': 0, 'member_count': guild_member_count, 'channels': []}

        guild_info[guild_id]['total_calls'] += 1
        guild_info[guild_id]['channels'].append(channel_name)

    print(total_personal_calls)
    print(total_guild_calls)

    for cmd in command_called_counter:
        print(cmd, ':', command_called_counter[cmd])
    print(len(guild_info))
    for inf in guild_info:
        print(guild_info[inf])


if __name__ == '__main__':
    analyse_command_logs()
