import os
current_dir = os.path.realpath(__file__)
current_dir = os.path.dirname(current_dir)
log_dir = os.path.join(current_dir, 'logs')
if not os.path.exists(log_dir):
    os.mkdir(log_dir)


IMAGE_SHIELD_JSON_FILE = os.path.join(log_dir, 'last_update_log.txt')
LOG_PATH = os.path.join(log_dir, 'command_logs.txt')

NEW_USER_SERVER_IMAGE_PATH = os.path.join(log_dir, 'new_user_server.jpg')
COMMAND_CALLS_IMAGE_PATH = os.path.join(log_dir, 'command_calls.jpg')
COMMAND_STATS_IMAGE_PATH = os.path.join(log_dir, 'command_stats.jpg')


