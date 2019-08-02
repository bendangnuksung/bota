from pyppeteer import launch
import asyncio


async def get_screenshot(selector, url, save_path):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    await page.tap(selector)
    await page.screenshot({'path': save_path})
    await browser.close()


if __name__ == '__main__':
    url = 'https://www.dotabuff.com/heroes/kunkka/builds'
    TALENT_SELECTOR = 'body > div.container-outer.seemsgood > div.container-inner.container-inner-content > div.content-inner > div.row-12.hero-abilities > div.col-8 > section:nth-child(1) > article > table'

    url = 'https://www.dotabuff.com/heroes/wraith-king/guides'
    ITEM_SELECTOR = 'body > div.container-outer.seemsgood > div.container-inner.container-inner-content > div.content-inner > section:nth-child(3) > article > div > div.top-right > div:nth-child(1)'

    path_to_save_screenshot = 'example.png'
    asyncio.get_event_loop().run_until_complete(get_screenshot(ITEM_SELECTOR, url, path_to_save_screenshot))
    import matplotlib.pyplot as plt
    import cv2
    image = cv2.imread(path_to_save_screenshot)
    # image = cv2.resize(image, (800, 350))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image)
    plt.show()
