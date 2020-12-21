import cv2
import requests, json
import base64
import io
from imageio import imread
from bota.logs_process.log_utils import extract_info
from bota.private_constant import LOG_PORCESS_IP_ADDRESS
from bota.logs_process import log_constant
from datetime import datetime
from bota.logs_process.log_utils import LogBackup

BASE_URL = LOG_PORCESS_IP_ADDRESS if LOG_PORCESS_IP_ADDRESS is not None else "http://0.0.0.0:5000/"
LAST_UPDATE_TIME = 0

log_backup = LogBackup()


def save_log(message, command_called):
    log = extract_info(message, command_called)
    p = log_constant.API_PATH_SAVELOG
    url_components = [BASE_URL, p]
    url = '/'.join(s.strip('/') for s in url_components)
    data = {'log': log}
    flag = True
    r = None

    try:
        r = requests.post(url, data=data)
    except requests.exceptions.RequestException as e:
        flag = False
        log_backup.append_log(log, e)
        print("*" * 50)
        print("Failed Saving logs: ", e)
        print("*" * 50)

    if flag and r.status_code == 200:
        if log_backup.is_fail_logs_in_memory():
            failed_logs = log_backup.get_failed_logs()
            for log in failed_logs:
                data = {'log': log}
                requests.post(url, data=data)
            log_backup.clear_failed_logs()
        return True
    else:
        return False


def get_command_log_tail(n):
    p = log_constant.APU_PATH_TAIL
    url_components = [BASE_URL, p]
    url = '/'.join(s.strip('/') for s in url_components)
    data = {'n': n}
    r = requests.post(url, data=data)
    r = json.loads(r.content)
    r = r['tail']
    return r


def get_stat_all_time():
    p = log_constant.API_PATH_ALL_TIME
    url_components = [BASE_URL, p]
    url = '/'.join(s.strip('/') for s in url_components)
    try:
        r = requests.post(url)
        r = json.loads(r.content)
        return r
    except requests.exceptions.RequestException as e:
        print("*"*50)
        print("Failed All time stats: ", e)
        print("*" * 50)
        return {}


def get_stat_new_user_server(n):
    p = log_constant.API_PATH_NEW_USER_SERVER
    url_components = [BASE_URL, p]
    url = '/'.join(s.strip('/') for s in url_components)
    data = {'n': n}
    r = requests.post(url, data=data)
    r = json.loads(r.content)
    summary = r.get('summary')
    image = r.get('image')
    if image is not None:
        image = base64.b64decode(image)
        image = imread(io.BytesIO(image))
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(log_constant.NEW_USER_SERVER_IMAGE_PATH, image)
    return log_constant.NEW_USER_SERVER_IMAGE_PATH, summary


def get_stat_commands(n):
    p = log_constant.API_PATH_COMMANDS
    url_components = [BASE_URL, p]
    url = '/'.join(s.strip('/') for s in url_components)
    data = {'n': n}
    r = requests.post(url, data=data)
    r = json.loads(r.content)
    summary = r.get('summary')
    image = r.get('image')
    if image is not None:
        image = base64.b64decode(image)
        image = imread(io.BytesIO(image))
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(log_constant.NEW_USER_SERVER_IMAGE_PATH, image)

    return log_constant.NEW_USER_SERVER_IMAGE_PATH, summary


def get_stat_calls(n):
    p = log_constant.API_PATH_CALLS
    url_components = [BASE_URL, p]
    url = '/'.join(s.strip('/') for s in url_components)
    data = {'n': n}
    r = requests.post(url, data=data)
    r = json.loads(r.content)
    summary = r.get('summary')
    image = r.get('image')
    if image is not None:
        image = base64.b64decode(image)
        image = imread(io.BytesIO(image))
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(log_constant.CALL_IMAGE_PATH, image)

    return log_constant.CALL_IMAGE_PATH, summary


def stats_update():
    p = log_constant.API_PATH_UPDATE
    url_components = [BASE_URL, p]
    url = '/'.join(s.strip('/') for s in url_components)
    r = None
    try:
        r = requests.post(url)
        r = json.loads(r.content)
        flag = r.get('flag')
        return flag
    except requests.exceptions.RequestException as e:
        print("*" * 50)
        print("Failed Stats update: ", e)
        print("*" * 50)
        return False


def update_value_to_server(force_update=False):
    global LAST_UPDATE_TIME
    url_components = [BASE_URL, log_constant.API_PATH_IMAGE_SHIELD_UPDATE]
    tp_url = '/'.join(s.strip('/') for s in url_components)

    current_time = datetime.now()
    if LAST_UPDATE_TIME == 0 or ((current_time - LAST_UPDATE_TIME).total_seconds() >= log_constant.UPDATE_AFTER) or force_update:
        stats_update()
        info = get_stat_all_time()
        user_no = info['Total Users']
        guild_no = info['Total Guilds']
        data = {'guilds': guild_no, 'users': user_no}
        try:
            requests.post(url=tp_url, data=data)
            LAST_UPDATE_TIME = current_time
            # print("Update to Log server  Successful")
        except requests.exceptions.ConnectionError:
            status_code = "Connection refused to Log server"
            # print(status_code)


if __name__ == '__main__':
    r = get_stat_all_time()
    print(r)