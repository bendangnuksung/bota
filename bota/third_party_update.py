# This script is just to show Image shield in Github (Personal purpose)
import requests
from datetime import datetime
from bota.private_constant import LOG_PORCESS_IP_ADDRESS

ip_address = LOG_PORCESS_IP_ADDRESS if LOG_PORCESS_IP_ADDRESS is not None else "http://localhost:5000/"
path = 'updatestat'
tp_url = ip_address + path


LAST_UPDATE_TIME = 0
UPDATE_AFTER = 21600 # update every 6 hours


def update_value_to_server(logstat, force_update=False):
    if ip_address == '':
        return
    global tp_url, LAST_UPDATE_TIME, UPDATE_AFTER
    current_time = datetime.now()
    if LAST_UPDATE_TIME == 0 or ((current_time - LAST_UPDATE_TIME).total_seconds() >= UPDATE_AFTER) or force_update:
        logstat.update_df()
        info = logstat.all_time()
        user_no = info['Total Users']
        guild_no = info['Total Guilds']
        data = {'guilds': guild_no, 'users': user_no}
        try:
            requests.post(url=tp_url, data=data)
            LAST_UPDATE_TIME = current_time
            print("update Successful")
        except requests.exceptions.ConnectionError:
            status_code = "Connection refused"
            print(status_code)
