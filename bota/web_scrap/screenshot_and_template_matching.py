import os
import random

import cv2
from bota import constant
import numpy as np
import shutil
import matplotlib.pyplot as plt
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys
from datetime import datetime


blank_template_image = cv2.imread(constant.BLANK_TEMPLATE_IMAGE, 0)
current_file_path = os.path.dirname(os.path.realpath(__file__))


def display(img):
    plt.imshow(img)
    plt.show()


# # https://stackoverflow.com/questions/55231170/taking-a-screenshot-of-a-web-page-in-pyqt5
# class Screenshot(QWebEngineView):
#     def capture(self, url, output_file):
#         self.output_file = output_file
#         self.load(QUrl(url))
#         self.loadFinished.connect(self.on_loaded)
#         # Create hidden view without scrollbars
#         self.setAttribute(Qt.WA_DontShowOnScreen)
#         self.page().settings().setAttribute(
#             QWebEngineSettings.ShowScrollBars, False)
#         self.show()
#
#     def on_loaded(self):
#         size = self.page().contentsSize().toSize()
#         self.resize(size)
#         # Wait for resize
#         QTimer.singleShot(1000, self.take_screenshot)
#
#     def take_screenshot(self):
#         self.grab().save(self.output_file, b'PNG')
#         self.app.quit()
#
#
# app = QApplication([])
# s = Screenshot()
# s.app = app


driver = None
vpn_driver = False
# vpn_driver = True


def get_html_using_vpn(url):
    global driver, vpn_driver
    if vpn_driver is False:
        destroy_sel_driver()
        vpn_driver = not vpn_driver

    if driver is None:
        initialise_sel_driver()

    driver.get(url)
    text = driver.page_source
    return text
    # soup = bs(driver.page_source, 'html.parser')


def get_my_ip(driver):
    print("Getting IP info ....")
    url = 'https://www.ipaddress.my/'
    driver.get(url)
    soup = bs(driver.page_source, 'html.parser')
    table = soup.find('table', {'class': 'table'})
    list = table.find_all('tr')

    text = []
    wanted_index = [0, 5, 12] # 0: IP, 5: Country, 12: Proxy host
    try:
        for i, l in enumerate(list):
            if i in wanted_index:
                value = l.find_all('td')
                key = str(value[0].string)
                value = str(value[1].string)
                key_value = f"{key} : {value}"
                text.append(key_value)
    except Exception as e:
        print("Failed in IP info: ", e)

    text = "\n".join(text)
    return text


def get_extension_url(soup, extension_name, html_pagename):
    extensions = soup.find_all('span', {'class': 'mrName', 'title': 'WebExtensions that are active in this session'})
    final_url = None
    for ext in extensions:
        text = ext.text
        text = text.strip()
        texts = text.split(',')
        name = texts[1]
        if extension_name in name:
            url_text = texts[2]
            url = url_text.replace('baseURL=', '')
            url = url[:-1] + html_pagename
            final_url = url
            break
    return final_url


def zenmate_connect(soup, driver):
    try:
        print("CONNECTING TO ZENMATE")
        final_url = get_extension_url(soup, 'ZenMate', "index.html")

        driver.get(final_url)
        driver.get(final_url)
        driver.get(final_url)
        driver.get(final_url)
        # xpath = "/html/body/app-root/main/app-home/div/div[2]/div[3]/a"
        # element = driver.find_element_by_xpath(xpath)

        element = driver.find_element_by_class_name('inactive-shield')
        driver.execute_script("arguments[0].click();", element)

        time.sleep(3.5)
        element.click()
        print("✓ SUCCESSFUL ✓")
        return True, ''
    except Exception as e:
        print("✖ FAILED ✖: ", e)
        return False, e


def hoxx_connect(soup, driver):
    email = "botahoxx@gmail.com"
    passwd = "bota@123"
    print("CONNECTING TO HOXX")
    try:
        final_url = get_extension_url(soup, 'Hoxx VPN Proxy', "popup.html")
        driver.get(final_url)
        time.sleep(0.5)

        language_xpath = '/html/body/div/div[1]/div[2]/div/div[2]/ul/li[1]'
        start = datetime.now()
        max_wait_language_popup = 30
        while True:
            try:
                driver.find_element_by_xpath(language_xpath).click()
                break
            except:
                time_taken = (datetime.now() - start).total_seconds()
                if time_taken > max_wait_language_popup:
                    break
                else:
                    continue
        time.sleep(1)

        username_xpath = '//*[@id="email-input"]'
        passwd_xpath = '//*[@id="password-input"]'
        login_xpath = '/html/body/div/div/div[2]/div[1]/div[3]/button/span'

        language_xpath = '/html/body/div/div[1]/div[2]/div/div[2]/ul/li[1]'
        start = datetime.now()
        max_wait_login_popup = 5
        while True:
            try:
                driver.find_element_by_xpath(username_xpath).send_keys(email)
                driver.find_element_by_xpath(passwd_xpath).send_keys(passwd)
                driver.find_element_by_xpath(login_xpath).click()
                break
            except:
                time_taken = (datetime.now() - start).total_seconds()
                if time_taken > max_wait_login_popup:
                    break
                else:
                    continue
        time.sleep(0.5)

        soup = bs(driver.page_source, 'html.parser')
        free_server_list = soup.find('ul', {'id': 'free-serverlist-ul'})
        regions = free_server_list.find_all('li')
        regions_ids_names = {}

        for region in regions:
            id = region.attrs['id']
            region_name = region['serverlabel']
            # regions_ids_names.append([id, region_name])
            regions_ids_names[region_name.lower()] = id

        wanted_region_sequence = ['singapore', 'germany', 'japan']
        wanted_region = list(regions_ids_names.keys())[0]
        for r in  wanted_region_sequence:
            if r in regions_ids_names:
                wanted_region = r
                break

        server_xpath = f'//*[@id="{regions_ids_names[wanted_region]}"]'
        select_region = wanted_region

        driver.find_element_by_xpath(server_xpath).click()
        time.sleep(7)

        # server_id_list =
        print("Connnected to ", select_region)
        print("✓ SUCCESSFUL ✓")
        return True, ""
    except Exception as e:
        print("✖ FAILED ✖ :", e)
        return False, e


def close_tabs(driver, n):
    # close all other tabs
    # num_of_tabs = 3 if vpn_driver else 2
    for x in range(1, n):
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'W')


def activate_vpn(driver, firefox=False):
    if not firefox:
        driver.get('chrome-extension://fdcgdnkidjaadafnichfpabhfomcebme/index.html')
        driver.get('chrome-extension://fdcgdnkidjaadafnichfpabhfomcebme/index.html')
        driver.get('chrome-extension://fdcgdnkidjaadafnichfpabhfomcebme/index.html')
        driver.get('chrome-extension://fdcgdnkidjaadafnichfpabhfomcebme/index.html')
        element = driver.find_element_by_xpath("/html/body/app-root/main/app-home/div/div[2]/div[3]/a/img[1]")
        time.sleep(2.5)
        element.click()

    if firefox:
        driver.get("about:memory")
        time.sleep(1.5)
        n_tabs = len(driver.window_handles)
        if n_tabs > 1:
            close_tabs(driver, n_tabs)
        while True:
            try:
                driver.find_element_by_xpath('//*[@id="measureButton"]').click()
                break
            except:
                continue

        time.sleep(1.5)
        source = driver.page_source
        soup = bs(source, 'html.parser')

        flag, exception_summary = zenmate_connect(soup, driver)
        if not flag:
            flag, exception_summary = hoxx_connect(soup, driver)

    ip_info = get_my_ip(driver)
    print("#"*30)
    print(ip_info)
    print("#" * 30)


def initialise_sel_driver(firefox=True, headless=False):
    global driver, vpn_driver
    if driver is None:
        if firefox:
            options = Options()
            options.headless = headless
            driver = webdriver.Firefox(options=options)
            driver.install_addon(constant.FIREFOX_AD_BLOCK)
            driver.install_addon(constant.FIREFOX_ZENMATE, temporary=True)
            driver.install_addon(constant.FIREFOX_IDC_COOKIES, temporary=True)
            driver.install_addon(constant.FIREFOX_HOXX, temporary=True)
            driver.get("about:support")
            addons = driver.find_element_by_xpath('//*[contains(text(),"Add-ons") and not(contains(text(),"with"))]')
            # scrolling to the section on the support page that lists installed extension
            driver.execute_script("arguments[0].scrollIntoView();", addons)
            close_tabs(driver, 2)

            if vpn_driver or headless is False:
                print("@" * 40)
                print("Activating VPN: ")
                activate_vpn(driver, firefox=True)
                print("@" * 40)
            else:
                print("@" * 40)
                print('VPN Disabled')
                print("@" * 40)

        else:
            # options = Options()
            # # options.headless = True
            # options.add_argument('--headless')
            # driver = webdriver.Chrome(chrome_options=options)
            # options = webdriver.ChromeOptions()

            chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_argument("--window-size=1920,1080")
            # chrome_options.add_argument("--disable-extensions")
            # chrome_options.add_argument("--proxy-server='direct://'")
            # chrome_options.add_argument("--proxy-bypass-list=*")
            # chrome_options.add_argument("--start-maximized")
            # # chrome_options.add_argument('--headless')
            # chrome_options.add_argument('--disable-gpu')
            # chrome_options.add_argument('--disable-dev-shm-usage')
            # chrome_options.add_argument('--no-sandbox')
            # chrome_options.add_argument('--ignore-certificate-errors')
            # options.chrome_options('--headless')

            # chrome_options.add_extension('/home/ben/Downloads/zenmate.crx')
            chrome_options.add_argument('--headless')
            driver = webdriver.Chrome(options=chrome_options)
            activate_vpn(driver)
            pass
            # driver.get('chrome-extension://fdcgdnkidjaadafnichfpabhfomcebme/index.html')


def destroy_sel_driver():
    global driver
    if driver is not None:
        driver.quit()
        del driver
        driver = None


def sel_screenshot(url, save_path, switch_mode=False):
    global driver, vpn_driver

    if switch_mode:
        destroy_sel_driver()
        vpn_driver = not vpn_driver

    if driver is None:
        initialise_sel_driver()
    driver.get(url)
    el = driver.find_element_by_tag_name('body')
    el.screenshot(save_path)


def take_screenshot(url, path_to_save, mode='sel'):
    # global s, app
    flag = True
    summary = ''
    dirname = os.path.dirname(path_to_save)
    filename_generated = url.replace('.com/', '.com_443/').replace('://', '_').replace('/', '_') + '.png'

    try:
        if mode == 'chromium':
            os.system(f'webscreenshot -r chromium --window-size 1200,5000 {url} -o {dirname}')
            # image = cv2.imread(os.path.join(dirname, filename_generated))
            # bad_image_flag = is_template_exists(image, blank_template_image)

        elif mode == 'phantomjs':
            os.system(f'webscreenshot {url} -o {dirname}')

        elif mode == 'sel':
            filename_generated = os.path.basename(path_to_save)
            sel_screenshot(url, path_to_save)
            screenshot_flag = is_screenshot_good(path_to_save)
            if not screenshot_flag:
                sel_screenshot(url, path_to_save, switch_mode=True)

        shutil.move(os.path.join(dirname, filename_generated), path_to_save)

    except Exception as e:
        flag = False
        summary = e

    return flag, summary


def is_template_exists(image, template_image, threshold=0.8):
    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if len(template_image.shape) > 2:
        template_image = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(image, template_image, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    exists = False
    for _ in zip(*loc[::-1]):
        exists = True
        break
    return exists


def is_screenshot_good(file_path, min_size=127098):
    file_size = os.path.getsize(file_path)
    if file_size < min_size:
        return False
    return True


def get_template_match_coords(image, template_image, threshold=0.4):
    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if len(template_image.shape) > 2:
        template_image = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(image, template_image, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    xmin = 0
    ymin = 0
    for pt in zip(*loc[::-1]):
        xmin = pt[0]
        ymin = pt[1]
        break
    return xmin, ymin


def crop_screenshots(image, template_image, offset_x, offset_y, offset_width, offset_height, threshold=0.7):
    x, y = get_template_match_coords(image, template_image, threshold=threshold)
    # cv2.rectangle(image, (x, y), (x + template_image.shape[1], y + template_image.shape[0]), (0, 255, 0), 2)
    # display(image)
    xmin = x + offset_x
    ymin = y + template_image.shape[0] + offset_y
    xmax = xmin + offset_width
    ymax = ymin + offset_height

    final_image = image[ymin:ymax, xmin:xmax]
    return final_image


if __name__ == '__main__':
    from bota import constant
    from bota.web_scrap.scrap_constant import heroes_names

    talent_template_image = cv2.imread(constant.TALENT_TEMPLATE_PATH, 0)
    skill_template_image = cv2.imread(constant.SKILL_TEMPLATE_PATH, 0)
    meta_template_image = cv2.imread(constant.META_TEMPLATE_IMAGE, 0)

    test_type = 'talent' # skill, talent, meta
    save_image = True
    is_display = True

    # crop_coords= skill_coords
    for hero_name in heroes_names:

        # hero_name = 'outworld-devourer'
        print(hero_name)

        if test_type == 'skill':
            x = constant.SKILL_OFFSET_X
            y = constant.SKILL_OFFSET_Y
            height = constant.SKILL_OFFSET_HEIGHT
            width = constant.SKILL_OFFSET_WIDTH
            template_image = skill_template_image
            url = constant.GUIDE_URL_SKILL.replace('<hero_name>', hero_name)
            path_to_save = os.path.join('temp/', hero_name+'_skill.png')

        elif test_type == 'talent':
            x = constant.TALENT_OFFSET_X
            y = constant.TALENT_OFFSET_Y
            height = constant.TALENT_OFFSET_HEIGHT
            width = constant.TALENT_OFFSET_WIDTH
            template_image = talent_template_image
            url = constant.GUIDE_URL_TALENT.replace('<hero_name>', hero_name)
            path_to_save = os.path.join('temp/', hero_name + '_talent.png')

        else:
            x = constant.META_OFFSET_X
            y = constant.META_OFFSET_Y
            height = constant.META_OFFSET_HEIGHT
            width = constant.META_OFFSET_WIDTH
            template_image = meta_template_image
            url = constant.META_URL
            path_to_save = os.path.join('temp/meta.png')

        take_screenshot(url, path_to_save)
        image = cv2.imread(path_to_save)

        cropped_image = crop_screenshots(image, template_image, x, y, offset_height=height, offset_width=width)

        if test_type == 'meta':
            xmin, ymin, xmax, ymax = constant.META_HERO_SPLIT_1_COORDS
            image_1 = cropped_image[ymin:ymax, xmin:xmax]
            display(image_1)

            xmin, ymin, xmax, ymax = constant.META_HERO_SPLIT_2_COORDS
            image_2 = cropped_image[ymin:ymax, xmin:xmax]
            display(image_2)

            cropped_image = np.concatenate([image_1, image_2], axis=1)

        if save_image:
            cv2.imwrite(path_to_save, cropped_image)

        if is_display:
            cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
            display(cropped_image)

        if test_type == 'meta':
            break
