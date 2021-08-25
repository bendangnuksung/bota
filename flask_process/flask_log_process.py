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


def save_command_logs(log):
    command_logger.info(log)


def get_command_log_tail(n):
    lines = []
    path = logs_constant.LOG_PATH
    with open(path) as f:
        file = f
    for i, line in enumerate(reversed(list(file))):
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
