from urllib.request import urlopen
from bota.bota_tv.decrypt_process import decrypt
import json
import random
import os


ENCRYPTED_KEYS = {'yt 22': 'h7GLVHY02BY/vWH6y11YJZeLsx7NkegS5U96pema9//cezu3oUD0Wh6Ps6o0hmX/+qAL3KaG6lvRE794aFh/8A==', 'yt 21': 'hwpQn7QkEjfCNfD7bwaieDt1ihA94C1Makr/vSbUediMA7X+l6bdwX2b/bFxEXV+pQF1t8cv3Wj+ZAghJ/kqeA==', 'yt 20': '/2ORWfoOweDGP4Ngt43b6m7mqTFnV8r209ypcOWdDDzkVo2OnQ24yIF7K8YMzObp1sYEvfZOZtffMchzApE4Sw==', 'yt 19': 'a+Tr+0w5HmKc7z3lLrukov8fqP7HweeaPA5BnBZXlatCiLQAJQzz7fwNFFe6NiMQXyGUuz83/sGKlluZO0IbnA==', 'yt 18': 'aIqPreLqpLs6jiXAlUnABuhubYrjZDM6FX2yOY8YnoDxNLxZCoaG+6Cm1CRuDi3liJdbhaXJoLzTIOF//pH1RQ==', 'yt 17': 'Xcdd+3X2CUkoaEyoLmFaSAf1UPGimNcVdf7LtF1M6SKG2tJ8godNAeVUAghoT5IwnkDpq+cGX8KsLQpyjGviQg==', 'yt 16': 'HOuxT81OK/uQv8WbqmEXeU8dLkbFfMbgDwaPEIBhxCi/Q1Cz/82b/+ozDf9DbR94vefkD3BX0Z6PFI4p9Ibabw==', 'yt 15': 'lpXEa7fEvzsjojLA/k+hOYknHQ/iWvvAt7FfMJJJlj8F/Ojziqfhbg9u9jeQWBFvkh0xodNq6XFriJUQmdroIA==', 'yt 14': '7PspBq1z31oL5CWr42XeqY1IG4pvxgRgVWnnY7OVAXzmxPDtRMSG+5lpHPZwYNrEK1af85KCH3BjSotTHa54wg==', 'yt 13': 'rkqmLXiw2LiXjN7weZatATxuU60onOrPKkjuzh5MAqm4fw/05JbVC6GIBwjIpmp2Y6FaUujE1eKj/8tJeHbaxA==', 'yt 12': 'RQVMGWg+0Q4xRn7r2bmNsFTgkycbPinqZ5pReDxrN+W4vtW1qrSj2VWgxs1oWkpE8rvWcLvm3n05PWAT+BywxA==', 'yt 11': 'TrXhxbUSu2t9e0SyxLMz9asSngDpdgvyYNtuJMno/Ss3AJ7dXbekuVXmU1Z01dxBwDheODNgbSw6W1CF/BFCEg==', 'yt 10': 'qXUFipl309GkMKqz8awB4/9UUPUaoQZWJLJNe3v+QOEJJ6tGL5w7Zhga00JSbI25tezflkeGMoshpKQLYvavJw==', 'yt 9': 'lFQ96annfC0gzWcB48zsf7DPuYlMSI5BMpaGZQzhKeXTPUHhnhp+OwQe4YM3y0+8pa9fxkN0p0klBlV5FKtPtA==', 'yt 8': 'dkH4Gx/HwK1mGySXZ+fnNWlDZqsSLKw3zQ3RH0RhWTOCgvPjzYwmBvmX8JV2qIDC/qaNEL+9ToShS7fP5LKytg==', 'yt 7': '7p37ui2CGos4IPzHbVhaOeEafX30p7YN19OijCnfEuqt315uILd/39a/UaWSeiEPrcrkNxH/c75w/GWCqrQ69w==', 'yt 6': 'klbFO3tfBWDZ8NXm+GtZQe87k+mAVJ1zKIuJnoJGBvhFgZCliKXEkdWjWe7ksDKgfJSWC6tJCtGK/VJg6jFKWQ==', 'yt 5': 'ztjLDbfx4gVNVd308p9R8fxx9IWP4IXcp7/t26zDe26DeYNi2otMdqI/4QUAu/mXiQE8oHQmg5eHrXk8W02gtA==', 'yt 4': 'M5Wywi7uePzStlDMLxtPRuQKB3K4kHsKd1xwulKoeDMAKZ5/5mvk44bCa46C1F6PejTXLTI26s+l5o8eszjj9g==', 'yt 3': 'fDKSP0HphtsrA9EjFjrnUh27zrLW3zM4yk2MuVTAmwI8+0VzV7v3/rZMe6WVAnZNFj91/mKXucdDyx9gcb5+Jw==', 'yt 2': 'B886twKtLesav64AwdsIqg99tGphaswCYd3jv7qolNV20oxQnaBrfnGR5J1lnuLyMgWSsp12O93JE+kDdh569g==', 'yt 1': '34mOd17Zcc4VvGho6ijPNDpLm8cbSzZEvjFPvOS/jX4RDssLfe0TibG6OWR4ICqyZ+ARyRMf9XxEyc81IeRGKA==', 'yt': 'kzLB/pO7hCHlEe1W2vIPOlyxLdIulXDwD6fgq+Ykw3uuqjEHurI4CgeVPBe9iFJJramEuJOIekvl1GfNPtLsJA==', 'botatv': 'TIIYSJX2RGYphsya4g+9dGytVj+XLIdnhKDcv2LtMtfTxU06a8V8Gkegh1CeAJU+wEz9Sa0gtvsSULBomR7vFw==', 'my first project': 'Q5RoUPxLORRS4bmCxMCOMrl3solSF67yraSOaVBAHsGT3hYNSnJ1DxaOLtFLicvZ0/k+URaF82Kg/T20LyMuzA=='}
channel_id = "UCnby5VqRpcJ-qzyhAp2cTAQ"


class YoutubeVideo:

    def __init__(self, encrypt_key=None, api_keys=ENCRYPTED_KEYS, channel_id=channel_id, limit=30):
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
        inp = urlopen(url)
        resp = json.load(inp)
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

        while True:
            inp = urlopen(url)
            resp = json.load(inp)

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
        return video_infos


if __name__ == '__main__':
    ytvideo = YoutubeVideo(encrypt_key="botadiscordbendangimsong@gmail.com")
    r = ytvideo.get_all_video_info_in_channel()
    print(r)
