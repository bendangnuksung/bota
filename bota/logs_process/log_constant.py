import os
current_dir = os.path.realpath(__file__)
current_dir = os.path.dirname(current_dir)
log_image_dir = os.path.join(current_dir, 'log_data')
if not os.path.exists(log_image_dir):
    os.mkdir(log_image_dir)


API_PATH_ALL_TIME = '/stats/all_time'
API_PATH_NEW_USER_SERVER = '/stats/new_user_and_server'
API_PATH_COMMANDS = '/stats/command'
API_PATH_CALLS = '/stats/calls'
API_PATH_UPDATE = '/stats/update'
API_PATH_SAVELOG = '/stats/update_command_log'
APU_PATH_TAIL = '/stats/tail'
API_PATH_IMAGE_SHIELD_UPDATE = 'updatestat'

UPDATE_AFTER = 21600 # update every 6 hours for image shield


ALL_TIME_IMAGE_PATH = os.path.join(log_image_dir, 'all_time.jpg')
NEW_USER_SERVER_IMAGE_PATH = os.path.join(log_image_dir, 'new_user_server.jpg')
COMMANDS_IMAGE_PATH = os.path.join(log_image_dir, 'commands.jpg')
CALL_IMAGE_PATH = os.path.join(log_image_dir, 'calls.jpg')


