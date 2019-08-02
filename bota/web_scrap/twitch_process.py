import requests
from bota import constant


def request_dota2_stream_json(url):
    response_flag = False
    response = {}
    for client_id in constant.TWITCH_CLIENT_IDS:
        r = requests.get(url, headers={constant.TWITCH_KEYWORD_CLIENT_ID: str(client_id)})
        if r.status_code == 200:
            response = r
            response_flag = True
            break

    if response_flag:
        return response.json()
    return response


def pretty_stream_text_for_discord(datas):
    final_string = '```diff\n' \
                   '-TOP DOTA 2 TWITCH STREAMS```'
    for i, data in enumerate(datas, 1):
        link = '<' + constant.TWITCH_URL + data[constant.TWITCH_KEYWORD_USER_NAME] + '>'
        final_string += f'{i}. **{data[constant.TWITCH_KEYWORD_USER_NAME]}**' \
                        f'    `VIEWS:`{data[constant.TWITCH_KEYWORD_VIEWER_COUNT]}' \
                        f'   `TITLE:` {data[constant.TWITCH_KEYWORD_TITLE]}' \
                        f' `LANG:` **{data[constant.TWITCH_KEYWORD_LANGUAGE].upper()}** \n`LINK`: {link}\n\n'
    return final_string


def get_dota2_top_stream(top=8):
    url = constant.TWITCH_DOTA_2_STREAM_URL + constant.DOTA_2_GAME_ID
    datas = request_dota2_stream_json(url)
    datas = datas[constant.TWITCH_KEYWORD_DATA]
    final_data = []
    for i, data in enumerate(datas):
        if i >= top:
            break
        final_data.append(data)
    result_string = pretty_stream_text_for_discord(final_data)
    return result_string


if __name__ == "__main__":
    print(get_dota2_top_stream())