from bs4 import BeautifulSoup
from markdown import markdown
import re
import requests
import os

from constant import REDDIT_DOTA_URL, JSON_POSTFIX, REDDIT_URL, REDDIT_POST_BODY, REDDIT_POST_TITLE, REDDIT_POST_AUTHOR, \
    REDDIT_POST_FLAIR, REDDIT_POST_SCORE, REDDIT_POST_URL, REDDIT_POST_MEDIA_URL, REDDIT_BODY_MAX_CHARACTER, \
    WEBPAGE_PRE_STRING, REDDIT_MAX_POST_LIMIT, REDDIT_DEFAULT_MODE, REDDIT_DEFAULT_TOP


def markdown_to_text(markdown_string):
    """ Converts a markdown string to plaintext """
    # md -> html -> text since BeautifulSoup can extract text cleanly
    html = markdown(markdown_string)
    # remove code snippets
    html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
    html = re.sub(r'<code>(.*?)</code >', ' ', html)
    # extract text
    soup = BeautifulSoup(html, "html.parser")
    text = ''.join(soup.findAll(text=True))
    return text


def make_dota2_url(sort_by, limit):
    if sort_by == 'hot':
        url = os.path.join(REDDIT_DOTA_URL, JSON_POSTFIX) + '?limit=' + str(limit)
        return url
    url = os.path.join(REDDIT_DOTA_URL, sort_by)
    url = os.path.join(url, JSON_POSTFIX) + '?limit=' + str(limit)
    return url


def is_content_webpage(string):
    for prefix in WEBPAGE_PRE_STRING:
        if string.startswith(prefix):
            return True
    return False


def pretty_reddit_text_to_list(dict_data):
    final_string_list = []
    for i, row in enumerate(dict_data):
        final_string = f'**{i+1}.** '
        for j, (key, value) in enumerate(row.items()):
            if j != 0:
                index_string_len = len(str(i))
                final_string += ' ' * (index_string_len + 3)
            if key == 'url':
                final_string += f"`{key.upper()}`: <{value}>    \n"
            elif key == 'content':
                final_string += f'`{key.upper()}:` '
                if is_content_webpage(value):
                    final_string += value
                else:
                    final_string += '\n'
                    final_string += '```fix' + "\n" + f"{value}" + '```'
            else:
                final_string += f"`{key.upper()}:` {value}    \n"
        final_string_list.append(final_string)
    return final_string_list


def scrap_reddit_dota(sort_by=REDDIT_DEFAULT_MODE, top=REDDIT_DEFAULT_TOP):
    top = top if top < REDDIT_MAX_POST_LIMIT else REDDIT_MAX_POST_LIMIT
    if sort_by == 'random':
        top = 1
        url = make_dota2_url(sort_by, top)
        r = requests.get(url, headers={'user-agent': 'Mozilla/5.0'})
        datas = r.json()
        datas = datas[0]['data']['children']
    else:
        url = make_dota2_url(sort_by, top)
        r = requests.get(url, headers={'user-agent': 'Mozilla/5.0'})
        datas = r.json()
        datas = datas['data']['children']

    result = []
    for i, data in enumerate(datas):
        if i > top:
            break
        data = data['data']
        title = data[REDDIT_POST_TITLE]
        flair = data[REDDIT_POST_FLAIR]
        author = data[REDDIT_POST_AUTHOR]
        score = data[REDDIT_POST_SCORE]
        url = REDDIT_URL + data[REDDIT_POST_URL]
        content = data[REDDIT_POST_BODY]
        if content != '':
            content = markdown_to_text(content)
            content = re.sub('[ ]+', ' ', content)
            content = re.sub('[\n]+', '\n', content)
            if len(content) > REDDIT_BODY_MAX_CHARACTER:
                content = content[:REDDIT_BODY_MAX_CHARACTER] + '.....'
        else:
            content = data[REDDIT_POST_MEDIA_URL]
        result.append({'title': title, 'flair': flair,
                       'score': score, 'url': url, 'content': content})
    result = pretty_reddit_text_to_list(result)
    return result


if __name__ == '__main__':
    r = scrap_reddit_dota('top')
    for x in r:
        print(x)
