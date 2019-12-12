import logging
from flask_process import logs_constant

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', '%Y-%m-%d %H:%M:%S')


def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


command_logger = setup_logger('command_logger', logs_constant.LOG_PATH)


def is_command_from_channel(message):
    channel = str(message.channel)
    if 'Direct Message' in channel:
        return False
    return True


def save_command_logs(message, command_called):
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
    command_logger.info(log_text)


def get_command_log_tail(n):
    lines = []
    path = logs_constant.LOG_PATH
    for i, line in enumerate(reversed(list(open(path)))):
        if i >=n:
            break
        line = f'{i+1}. ' + line
        line_split = line.split(',')
        first = line_split[0].replace('INFO', '')
        first = first.split('#')[0]
        line_taken = [first, line_split[4], line_split[5], line_split[6], line_split[9]]
        line = ", ".join(line_taken)
        lines.append(line)
    lines = "".join(lines)
    lines = f'```cs\n{lines}```'
    return lines
