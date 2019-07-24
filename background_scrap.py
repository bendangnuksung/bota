import schedule
import time
from web_scrap.scrap import get_item_build, get_skill_build
from web_scrap.scrap_constant import heroes_names
import asyncio
from datetime import datetime


def update_images():
    print("*"*80)
    print("UPDATING: ")
    loop = asyncio.get_event_loop()
    start = datetime.now()
    for i, hero_name in enumerate(heroes_names):
        print(f"{i + 1} / {len(heroes_names)}, Hero: {hero_name}")
        loop.run_until_complete(get_skill_build('', hero=hero_name))
        get_item_build('', hero=hero_name)
    end = datetime.now()
    print("*"*80)
    print("Update Completed")
    print(f"Total Time taken: {((end-start).total_seconds()) / 60} min")
    print("Start time: ", start.strftime('%H:%M:%S'))
    print("End time:   ", end.strftime('%H:%M:%S'))
    print("Date: ", start.strftime('%d-%m-%Y'))
    return


# UST 00:00 == IST 05:30
schedule.every().day.at("22:00").do(update_images)


while True:
    schedule.run_pending()
    time.sleep(60) # wait 1 minute
