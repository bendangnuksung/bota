import schedule
import time
from bota.web_scrap.scrap import get_item_build, get_skill_build, get_current_trend, get_counter_hero, get_good_against
from bota.web_scrap.scrap_constant import heroes_names
import asyncio
from datetime import datetime
import argparse
from argparse import RawTextHelpFormatter
import subprocess

parser = argparse.ArgumentParser(description='Script to scrap data everyday at a particular time',
                                 formatter_class=RawTextHelpFormatter,)

# parser.add_argument('--time', '-t', help='UST time at which update will take place. Format: HH:MM ', default='22:00')
parser.add_argument('--mode', '-m', help='1: Update images once a day at given time \n'
                                         '2: Update images now and returns back to mode 1',          default=1)
args = vars(parser.parse_args())


LAST_UPDATE = 0
UPDATE_INTERVAL = 60 # 1 min


def update_images():
    global LAST_UPDATE
    if LAST_UPDATE != 0:
        current_time = datetime.now()
        if (current_time - LAST_UPDATE).total_seconds() < UPDATE_INTERVAL:
            return

    print("*"*80)
    print("UPDATING: ")
    loop = asyncio.get_event_loop()
    start = datetime.now()
    get_current_trend()
    for i, hero_name in enumerate(heroes_names):
        print(f"{i + 1} / {len(heroes_names)}, Hero: {hero_name}")
        try:
            loop.run_until_complete(get_skill_build('', hero=hero_name, use_outdated_photo_if_fails=False))
        except Exception:
            subprocess.run(["pkill", "chrome"])
            pass
        try:
            get_item_build('', hero=hero_name, use_outdated_photo_if_fails=False)
            get_counter_hero('', hero=hero_name, use_outdated_photo_if_fails=False)
            get_good_against('', hero=hero_name, use_outdated_photo_if_fails=False)
        except Exception:
            continue
    end = datetime.now()
    print("*"*80)
    print("Update Completed")
    print(f"Total Time taken: {((end-start).total_seconds()) / 60} min")
    print("Start time: ", start.strftime('%H:%M:%S'))
    print("End time:   ", end.strftime('%H:%M:%S'))
    print("Date: ", start.strftime('%d-%m-%Y'))
    subprocess.run(["pkill", "chrome"])
    LAST_UPDATE = datetime.now()
    return


if args['mode'] == 2 or args['mode'] == '2':
    print("Running One Time update:")
    update_images()
    print("Finished One Time update")



while True:
    update_images()
    time.sleep(UPDATE_INTERVAL-5) # wait 1 minute
