import os
import cv2
from bota import constant
import numpy as np
import shutil
import matplotlib.pyplot as plt

current_file_path = os.path.dirname(os.path.realpath(__file__))


def display(img):
    plt.imshow(img)
    plt.show()


def take_screenshot(url, path_to_save):
    flag = True
    summary = ''
    dirname = os.path.dirname(path_to_save)
    filename_generated = url.replace('.com/', '.com_443/').replace('://', '_').replace('/', '_') + '.png'

    # print(dirname, ' | ', filename)
    # print(url)
    try:
        # os.system(f'webscreenshot {url} -o {dirname}')
        os.system(f'webscreenshot -r chromium --window-size 1200,5000 {url} -o {dirname}')
        shutil.move(os.path.join(dirname, filename_generated), path_to_save)

    except Exception as e:
        flag = False
        summary = e

    return flag, summary


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

    test_type = 'meta' # skill, talent, meta
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