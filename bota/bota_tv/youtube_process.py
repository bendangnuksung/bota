from urllib.request import urlopen
from bota.bota_tv.decrypt_process import decrypt
import json
import random
import os
import requests


ENCRYPTED_KEYS = {'cc:': '5ak0cUjgaeLxvMRLGf1nPd92fa8eAMVoP7uR+I8dp3DTp0oYme/+p4Bd2WBRb45VlC19/vkWlfw0XHU5O4YHsQ==', 'steam': 'P0FUsUP7te3tPALeHeN5jVbqkrhAOau0sN4SOs+mcJFbn797MJXUjPVoCkfxhoVgQUaGznrsWJetTdfXa3O6Eg==', 'bendang': '2FIwUsxVrwcLAnViznVrsGLbnH5RYH81+BF9BLKqCtYaE4RZnhD0hsXfMTI8Lrse/kQepsEWadkksdrOpGL+4w==', 'playing2': 'NulblAODU8FwExmh/iRT5Hr1ALr+tGhHy5lw2d2WcrePcaG8k77HQuyqIdXnmdFA+394l1J12Pq++lTltMl2bg==', 'bota': 'V/lXFlwVb5A3cfyQF83/dE215Zshc9YWuOKSKCJaZ7hSeVq6NCTDb7tI8jpOVKpN1sb2MKlJ9aEiAkQpP6OEIw==', 'playing1': 'yCWRin5NogBJOlaWHnFcNLhl7wS5/X9tMyzbbZO1pvRoCuh8IDmhT5PVY4y5Ur375lg+D9tHRmjadzL0tJ9UdQ==', 'playing': 'fw1lMg/M2casHtE8I9FhWPopSL5OtjFCiKdsE5mDyy0E+KyrRzT9E9ph6WD3dsZb7srP3F+KrUZlFYjTY5CSZw=='}
channel_id = "UCnby5VqRpcJ-qzyhAp2cTAQ"


class YoutubeVideo:

    def __init__(self, encrypt_key=None, api_keys=ENCRYPTED_KEYS, channel_id=channel_id, limit=40):
        self.encrypt_key = str.encode(encrypt_key) if encrypt_key is not None else self._load_encrypt_key()
        self.api_keys = self._load_api_keys(api_keys)
        self.channel_id = channel_id
        self.current_api_key_idx = 0
        self.limit = limit
        random.shuffle(self.api_keys)

        self.base_video_url = 'https://www.youtube.com/watch?v='
        self.base_search_url = 'https://www.googleapis.com/youtube/v3/search?'

    def _load_encrypt_key(self):
        env_var = os.environ
        ENCRYPT_KEY = env_var.get('ENCRYPT_KEY')
        ENCRYPT_KEY = str.encode(ENCRYPT_KEY)
        return ENCRYPT_KEY

    def _load_api_keys(self, keys):
        decrypt_api_keys = []
        for key, api_key in keys.items():
            api_key = decrypt(self.encrypt_key, api_key)
            api_key = api_key.decode()
            decrypt_api_keys.append(api_key)
        return decrypt_api_keys

    def get_api_key(self):
        idx = self.current_api_key_idx % len(self.api_keys)
        key = self.api_keys[idx]
        self.current_api_key_idx += 1
        return key

    def get_full_description(self, video_ids, apikey):
        video_ids_text = ",".join(video_ids)
        url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_ids_text}&key={apikey}'
        inp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = inp.json()
        descriptions = []

        for i in resp['items']:
            d = i['snippet']['description']
            descriptions.append(d)

        return descriptions

    def get_all_video_info_in_channel(self, channel_id=None):
        channel_id = self.channel_id if channel_id is None else channel_id

        video_infos = []
        api_key = self.get_api_key()
        first_url = self.base_search_url + 'key={}&channelId={}&part=snippet,id&order=date&maxResults={}'.format(
            api_key, channel_id, self.limit)
        url = first_url
        max_retry = 2
        current_retry = 0
        while True:
            resp = None
            while True:
                if current_retry > max_retry:
                    break
                inp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                resp = inp.json()
                got_items = False
                try:
                    for _ in resp['items']:
                        got_items = True
                        break
                    if got_items:
                        break
                except:
                    new_api_key = self.get_api_key()
                    url = url.replace(api_key, new_api_key)
                    api_key = new_api_key
                    current_retry += 1
                    print(current_retry)

            video_ids = []
            infos = []
            for i in resp['items']:
                if i['id']['kind'] == "youtube#video":
                    video_ids.append(i['id']['videoId'])
                    video_link = self.base_video_url + i['id']['videoId']
                    description = i['snippet']['description']
                    title = i['snippet']['title']
                    published = i['snippet']['publishedAt']
                    info = {'link': video_link,
                            'title': title,
                            'published': published,
                            'description': description}
                    infos.append(info)

            descriptions = self.get_full_description(video_ids, api_key)
            for i, description in enumerate(descriptions):
                infos[i]['description'] = description

            video_infos += infos

            try:
                new_api_key = self.get_api_key()
                next_page_token = resp['nextPageToken']
                url = first_url + '&pageToken={}'.format(next_page_token)
                url = url.replace(api_key, new_api_key)
                api_key = new_api_key
            except:
                break
        print("Finished fetching YT videos")
        return video_infos


if __name__ == '__main__':
    ytvideo = YoutubeVideo(encrypt_key="")
    r = ytvideo.get_all_video_info_in_channel()
    print(r)
