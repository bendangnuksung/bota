from bota.bota_tv.youtube_dl_process import YoutubeVideo
from bota.utility.general import is_file_old
from bota.web_scrap.scrap_constant import heroes_names, d2pt_hero_names
from bota import constant
from operator import itemgetter
import os
import json

ytvideo = YoutubeVideo()

stop_words = ['of', 'the']


def camel_case(txt):
    final_txt = []
    for word in txt.split():
        word = word[0].upper() + word[1:].lower()
        if "-" in word:
            words = word.split("-")
            word = words[0] + '-' + words[1][0].upper() + words[1][1:].lower()

        if word.lower() in stop_words:
            word = word.lower()
        final_txt.append(word)

    return " ".join(final_txt)


def extract_info(description):
    description = description.lower()
    description_lines = description.split("\n")
    heroname = None
    playername = None
    position = None
    mmr = None
    for line in description_lines:
        if line.startswith("hero"):
            heroname = line.split(":")[1]

        elif line.startswith("player"):
            playername = line.split(":")[1:]
            playername = ":".join(playername)

        elif line.startswith("mmr"):
            mmr = line.split(":")[1]

        elif line.startswith("position"):
            position = line.split(":")[1]

    return heroname, playername, position, mmr


def update_video_links(update_after=14000):
    file_path = constant.YT_LINK_PATH

    if os.path.exists(file_path) and not is_file_old(file_path, update_after):
        return False

    all_vid_info = ytvideo.get_video_links()
    videos_info = []
    hero_perspective_info = {}
    for heroname in heroes_names:
        heroname = d2pt_hero_names[heroname]
        hero_perspective_info[heroname] = []

    for vid_info in all_vid_info:
        heroname, playername, position, mmr = extract_info(vid_info['description'])
        if heroname is None:
            print("No hero name")
        heroname = camel_case(heroname)
        link = vid_info['link']
        published = vid_info['published']
        infos = {'heroname': heroname, 'player': playername, 'mmr': mmr, 'link': link, 'published': published,
                 'position': position}
        videos_info.append(infos)

    all_video_info = sorted(videos_info, key=itemgetter('published'), reverse=True)

    for info in all_video_info:
        heroname = info['heroname']
        hero_perspective_info[heroname].append(info)

    with open(file_path, 'w') as fp:
        json.dump(hero_perspective_info, fp, indent=4, default=str)

    with open(constant.ALL_YT_LINK_PATH, 'w') as fp:
        json.dump(all_video_info, fp, indent=4, default=str)

    return True


if __name__ == '__main__':
    update_video_links(1000)