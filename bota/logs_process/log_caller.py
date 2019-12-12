import discord
from bota import constant
import os
import cv2
import requests, json
import base64
import io
from imageio import imread
from bota.private_constant import LOG_PORCESS_IP_ADDRESS
from bota.logs_process import log_constant
from datetime import datetime

BASE_URL = LOG_PORCESS_IP_ADDRESS if LOG_PORCESS_IP_ADDRESS is not None else "http://0.0.0.0:5000/"
LAST_UPDATE_TIME = 0


def get_stat_all_time():
    p = log_constant.API_PATH_ALL_TIME
    url_components = [BASE_URL, p]
    url = '/'.join(s.strip('/') for s in url_components)
    r = requests.post(url)
    r = json.loads(r.content)
    return r


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
    print(r.content)
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
    r = requests.post(url)
    r = json.loads(r.content)
    flag = r.get('flag')
    return flag


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
            print("update Successful")
        except requests.exceptions.ConnectionError:
            status_code = "Connection refused"
            print(status_code)


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


if __name__ == '__main__':
    r = get_stat_all_time()
    print(r)