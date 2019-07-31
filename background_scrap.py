import schedule
import time
from web_scrap.scrap import get_item_build, get_skill_build, get_current_trend, get_counter_hero, get_good_against
from web_scrap.scrap_constant import heroes_names
import asyncio
from datetime import datetime
import argparse
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(description='Script to scrap data everyday at a particular time',
                                 formatter_class=RawTextHelpFormatter,)

parser.add_argument('--time', '-t', help='UST time at which update will take place. Format: HH:MM ', default='22:00')
parser.add_argument('--mode', '-m', help='1: Update images once a day at given time \n'
                                         '2: Update images now and returns back to mode 1',          default=1)
args = vars(parser.parse_args())


def update_images():
    print("*"*80)
    print("UPDATING: ")
    loop = asyncio.get_event_loop()
    start = datetime.now()
    for i, hero_name in enumerate(heroes_names):
        print(f"{i + 1} / {len(heroes_names)}, Hero: {hero_name}")
        loop.run_until_complete(get_skill_build('', hero=hero_name))
        get_item_build('', hero=hero_name)
        get_current_trend()
        get_counter_hero('', hero=hero_name)
        get_good_against('', hero=hero_name)
    end = datetime.now()
    print("*"*80)
    print(f"Background Scrapping process starts at: {arg_time_1} and  {arg_time_2} everyday")
    print("Update Completed")
    print(f"Total Time taken: {((end-start).total_seconds()) / 60} min")
    print("Start time: ", start.strftime('%H:%M:%S'))
    print("End time:   ", end.strftime('%H:%M:%S'))
    print("Date: ", start.strftime('%d-%m-%Y'))
    return


if args['mode'] == 2 or args['mode'] == '2':
    print("Running One Time update:")
    update_images()
    print("Finished One Time update")


# UST 00:00 == IST 05:30
# Twice a day: 12 Hours apart
arg_time_1 = args['time']
arg_time_1_split = arg_time_1.split(':')
arg_time_2_h = str((int(arg_time_1_split[0]) + 12) % 24)
arg_time_2_h = '0' + arg_time_2_h if len(arg_time_2_h) == 1 else arg_time_2_h
arg_time_2 = str(arg_time_2_h) + ':' + arg_time_1_split[1]


schedule.every().day.at(arg_time_1).do(update_images)
schedule.every().day.at(arg_time_2).do(update_images)

print(f"Background Scrapping process starts at: {arg_time_1} and  {arg_time_2} everyday")

while True:
    schedule.run_pending()
    time.sleep(60) # wait 1 minute
