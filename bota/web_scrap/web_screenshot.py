from pyppeteer import launch
import asyncio


async def get_screenshot(selector, url, save_path):
    browser = await launch({"args": ["--no-sandbox"]})
    flag = True
    exception_summary = ''
    try:
        page = await browser.newPage()
        await page.goto(url)
        await page.tap(selector)
        await page.screenshot({'path': save_path})
    except Exception as e:
        flag = False
        exception_summary = e
    finally:
        await browser.close()
        return flag, exception_summary


if __name__ == '__main__':
    'https://www.dotabuff.com/heroes/abaddon example.png'
    # url = 'https://www.dotabuff.com/heroes/kunkka/builds'
    # TALENT_SELECTOR = 'body > div.container-outer.seemsgood > div.container-inner.container-inner-content > div.content-inner > div.row-12 > div.col-8 > section:nth-child(5) > article'

    url = 'https://www.dotabuff.com/heroes/abaddon'
    ITEM_SELECTOR = 'body > div.container-outer.seemsgood > div.container-inner.container-inner-content > div.content-inner > div.row-12 > div.col-4 > section:nth-child(2) > article'

    path_to_save_screenshot = 'example.png'
    asyncio.get_event_loop().run_until_complete(get_screenshot(ITEM_SELECTOR, url, path_to_save_screenshot))
    import cv2
    image = cv2.imread(path_to_save_screenshot)
    from bota.utility.general import crop_image
    image = crop_image(image, [0, 155, 800, -150])
    cv2.imwrite(path_to_save_screenshot, image)

    import matplotlib.pyplot as plt
    import cv2
    image = cv2.imread(path_to_save_screenshot)
    # image = cv2.resize(image, (800, 350))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image)
    plt.show()
