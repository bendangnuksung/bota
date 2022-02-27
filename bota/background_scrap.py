import logging
from logging.handlers import RotatingFileHandler
import time
from bota.web_scrap.scrap import get_item_build, get_skill_build, get_current_trend, get_counter_hero, get_good_against, get_meta
from bota.web_scrap.scrap_constant import heroes_names, hero_role
from bota.web_scrap.screenshot_and_template_matching import destroy_sel_driver
from bota.constant import SCRAP_LOG_PATH
import asyncio
from datetime import datetime
import argparse
from argparse import RawTextHelpFormatter
import subprocess
from tqdm import tqdm


parser = argparse.ArgumentParser(description='Script to scrap data everyday at a particular time',
                                 formatter_class=RawTextHelpFormatter,)

# parser.add_argument('--time', '-t', help='UST time at which update will take place. Format: HH:MM ', default='22:00')
parser.add_argument('--mode', '-m', help='1: Update images once a day at given time \n2: Update images now and returns back to mode 1 \n3: Scrap Only once and stop', default=1)
args = vars(parser.parse_args())


LAST_UPDATE = 0
UPDATE_INTERVAL = 60 # 1 min
SCRAP_LOG_FILE_PATH = 'scrap_log.txt'

SCREEN_SHOT_SCRAP_FUNCTIONS = {'skill': get_skill_build, 'item': get_item_build,
                               'counter': get_counter_hero, 'good': get_good_against}
SCRAP_FUNCTIONS_THAT_NEED_LOOP = []

#
formatter = logging.Formatter('%(asctime)s - %(message)s', '%d-%m %H:%M')

EVEN_ONE_FAILED = False


def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""
    handler = RotatingFileHandler(log_file, mode='a', maxBytes=1024*128, backupCount=2, encoding=None)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


background_logger = setup_logger('background_logger', SCRAP_LOG_PATH)


def run_func_in_exception_block(hero_name, loop):
    global EVEN_ONE_FAILED
    for key, scrap_function in SCREEN_SHOT_SCRAP_FUNCTIONS.items():
        if key in SCRAP_FUNCTIONS_THAT_NEED_LOOP:
            returned_kwargs = loop.run_until_complete(scrap_function('', hero=hero_name, use_outdated_photo_if_fails=False))
        else:
            returned_kwargs = scrap_function('', hero=hero_name, use_outdated_photo_if_fails=False)
        flag, exception_reason = returned_kwargs[0], returned_kwargs[-1]
        if flag:
            log_info = f"\t{key} : SUCCESSFUL ✓"
            print(log_info)
            background_logger.info(log_info)
        else:
            log_info = f"\t{key} : FAILED ✖✖, Reason: {exception_reason}"
            EVEN_ONE_FAILED = True
            print(log_info)
            background_logger.info(log_info)
            subprocess.run(["pkill", "chrome"])


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
    meta_r = get_meta(early_update=True, use_outdated_photo_if_fails=False)
    meta_r = 'Unsuccessful' if meta_r is None else 'Success'
    meta_r = f"META: {meta_r}"
    background_logger.info(meta_r)
    for i, hero_name in enumerate(tqdm(heroes_names)):
        iter_text = f"{i + 1}/{len(heroes_names)}, Hero: {hero_name}"
        print(iter_text)
        background_logger.info(iter_text)
        run_func_in_exception_block(hero_name, loop)

    end = datetime.now()
    stats = f"{'*'*50} \n Update Completed \n" \
            f" Total Time taken: {((end-start).total_seconds()) / 60} min \n" \
            f"Start time: {start.strftime('%H:%M:%S')} \n" \
            f"End time: {end.strftime('%H:%M:%S')} \n" \
            f"Date: {start.strftime('%d-%m-%Y')} \n" \
            f"{'*'*50}"

    print(stats)
    background_logger.info(stats)
    subprocess.run(["pkill", "chrome"])
    LAST_UPDATE = datetime.now()
    destroy_sel_driver()
    return


print("MODE: ", args['mode'])
if args['mode'] == 2 or args['mode'] == '2' or args['mode'] == '3' or args['mode'] == 3:
    print("Running One Time update:")
    update_images()
    print("Finished One Time update")

    if (args['mode'] == '3' or args['mode'] == 3) and EVEN_ONE_FAILED:
        print("#"*50)
        print("One of the scrap functions failed. Exiting")
        print("#" * 50)
        exit(1)
    elif (args['mode'] == '3' or args['mode'] == 3) and not EVEN_ONE_FAILED:
        print("-" * 50)
        print("Successful One time Update")
        print("#" * 50)
        exit(0)

if args['mode'] != '3':
    while True:
        update_images()
        time.sleep(UPDATE_INTERVAL-5) # wait 1 minute
