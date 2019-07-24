import schedule
import time
from web_scrap.scrap import get_item_build, get_skill_build
from web_scrap.scrap_constant import heroes_names
import asyncio


def update_images():
    print("*"*80)
    print("UPDATING: ")
    loop = asyncio.get_event_loop()
    for i, hero_name in enumerate(heroes_names):
        if i % 5 == 0:
            print(f"{i + 1} / {len(heroes_names)} heroes")
        loop.run_until_complete(get_skill_build('', hero=hero_name))
        get_item_build('', hero=hero_name)
    return


schedule.every().day.at("18:16").do(update_images)


while True:
    schedule.run_pending()
    time.sleep(60) # wait 1 minute
