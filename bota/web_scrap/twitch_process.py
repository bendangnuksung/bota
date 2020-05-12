import requests

import bota.private_constant
from bota import constant


twitch_language = {'english': "en", "dansk": 'da', "danish": "da", "deutsch": "de", "german": 'de',
                   'español': 'es', 'espanol': 'es', 'spanish': 'es', 'français': 'fr',  'francais': 'fr', 'french': 'fr',
                   'italiano': 'it', 'italian': 'it', 'magyar': 'hu', 'hungarian': 'hu', 'nederlands': 'nl',
                   'netherland': 'nl', 'norsk': 'no', 'norwegian': 'no', 'polski': 'pl', 'polish': 'pl',
                   'português': 'pt', 'portuguese': 'pt', 'română': 'ro', 'romana': 'ro', 'romanian': 'ro',
                   'slovenčina': 'sk', 'slovak': 'sk', 'suomi': 'fi', 'finish': 'fi', 'svenska': 'sv', 'swedish': 'sv',
                    'tiếng việt': 'vi', 'vietnamese': 'vi', 'türkçe': 'tr', 'turkce': 'tr', 'turkish': 'tr',
                    'ceština': 'cs', 'czech': 'cs', 'eλληνικά': 'el', 'greek': 'el', 'български': 'bg', 'bulgarian': 'bg',
                   'pусский': 'ru', 'slovenian': 'ru', 'russian': 'ru', 'العربية': 'ar', 'arabic': 'ar',
                   'ภาษาไทย': 'th', 'thai': 'th', '中文': 'zh', 'chinese': 'zh', '中文 繁體': 'zh-hk', 'hong kong': 'zh-kh',
                   '日本語': 'ja', 'japanese': 'ja', '한국어': 'ko', 'korean': 'ko', 'sign': 'asl', 'ru': 'ru'}


def request_dota2_stream_json(url):
    response_flag = False
    response = {}
    for client_id, oth_token in bota.private_constant.TWITCH_AUTH_TOKENS.items():
        r = requests.get(url, headers={'Client-Id': str(client_id), "Authorization": "Bearer " + oth_token})
        # r = requests.get(url, headers={constant.TWITCH_KEYWORD_CLIENT_ID: str(client_id)})
        if r.status_code == 200:
            response = r
            response_flag = True
            break

    if response_flag:
        return response.json()
    return response


def pretty_stream_text_for_discord(datas, language):
    final_string = f"```diff\n-TOP DOTA 2 TWITCH STREAMS: LANGUAGE: {language}```\n"
    for i, data in enumerate(datas, 1):
        # title =
        link = constant.TWITCH_URL + data[constant.TWITCH_KEYWORD_USER_NAME]
        final_string += f'{i}. **{data[constant.TWITCH_KEYWORD_USER_NAME]}**' \
                        f'    `VIEWS:`{data[constant.TWITCH_KEYWORD_VIEWER_COUNT]}' \
                        f'   `TITLE:` _{(data[constant.TWITCH_KEYWORD_TITLE]).rstrip()}_  ' \
                        f' `LANG:` **{data[constant.TWITCH_KEYWORD_LANGUAGE].upper()}**' \
                        f'    __**[LINK]({link})**__\n\n'
    return final_string


def get_dota2_top_stream(language=None, top=8):
    url = constant.TWITCH_DOTA_2_STREAM_URL + constant.DOTA_2_GAME_ID
    language_used = 'ALL'
    if language is not None:
        if len(language) <= 3:
            language_used = language
            url += f"&language={language}"
        else:
            language = twitch_language.get(language)
            if language is not None:
                language_used = language
                url += f"&language={language}"

    datas = request_dota2_stream_json(url)
    datas = datas[constant.TWITCH_KEYWORD_DATA]
    final_data = []
    for i, data in enumerate(datas):
        if i >= top:
            break
        final_data.append(data)

    result_string = pretty_stream_text_for_discord(final_data, language_used.upper())
    return result_string


if __name__ == "__main__":
    print(get_dota2_top_stream())