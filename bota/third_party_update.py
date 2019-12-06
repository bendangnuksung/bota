# This script is just to show Image shield in GIthub (Personal)
import requests
from datetime import datetime


ip_address = ''
path = ''
tp_url = ip_address + path


LAST_UPDATE_TIME = 0
UPDATE_AFTER = 21600 # update every 6 hours


def update_value_to_server(logstat):
    if ip_address == '':
        return
    global tp_url, LAST_UPDATE_TIME, UPDATE_AFTER
    current_time = datetime.now()
    if LAST_UPDATE_TIME == 0 or ((current_time - LAST_UPDATE_TIME).total_seconds() >= UPDATE_AFTER):
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
