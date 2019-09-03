from bota.web_scrap.dotavoyance.dotavoyance import Dotavoyance
from bota.web_scrap.heroes_process import find_hero_name
from bota.image_processing import add_border_to_image, write_text_pil
import cv2
import os
from bota import constant

DV = Dotavoyance()
SORT_BY_KEYS = ['high', 'med', 'low']

TEAMMATE_BG_IMAGE = '/home/ben/personal/bota/bota/data/background/team_background.jpg'


def display(img):
    import matplotlib.pyplot as plt
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.show()


def make_teammate_image(my_heroes, results, bg_image=TEAMMATE_BG_IMAGE):
    bg_image = cv2.imread(bg_image)
    bg_h, bg_w, _ = bg_image.shape
    start_left = 50
    start_top = 150

    max = 10

    my_hero_start_top = 675
    my_hero_start_left = ((bg_w // 2) - 85) - (((len(my_heroes) -1) * 200) // 2)
    for i, hero_name in enumerate(my_heroes):
        hero_icon = cv2.imread(os.path.join(constant.ICON_PATH_BIG, hero_name + '.png'))
        hero_icon = add_border_to_image(hero_icon)
        icon_h, icon_w, _ = hero_icon.shape
        hero_icon_x = my_hero_start_top
        hero_icon_y = my_hero_start_left + (i * 200)
        bg_image[hero_icon_x: hero_icon_x + icon_h, hero_icon_y: hero_icon_y + icon_w, :] = hero_icon

    count = 0
    for i, result in enumerate(results):
        hero_names = result['heroes']
        for j, hero_name in enumerate(hero_names):
            if count >= 10:
                break
            hero_icon = cv2.imread(os.path.join(constant.ICON_PATH_BIG, hero_name + '.png'))
            icon_h, icon_w, _ = hero_icon.shape
            k = i + j
            if i % 2 == 1:
                hero_icon_x = start_top + (((k) // 2) * 90)
                print(hero_icon_x)
                hero_icon_y = start_left + 700
            else:
                hero_icon_x = start_top + (((k+1) // 2) * 90)
                hero_icon_y = start_left
            bg_image[hero_icon_x: hero_icon_x + icon_h, hero_icon_y: hero_icon_y + icon_w, :] = hero_icon

            win_rate_x = hero_icon_x + (icon_h // 3)
            win_rate_y = hero_icon_y + (icon_w // 2) + 275
            percen = str(result['win_percentage']) + '%'
            pos = (win_rate_y, win_rate_x)
            bg_image = write_text_pil(bg_image, percen, pos, size=30)
            count += 1

        # break
    cv2.imwrite('/home/ben/Desktop/test.jpg', bg_image)
    display(bg_image)
    return bg_image


def extract_heroname_sortby(arguments):
    hero_names = []
    sort_by = ''
    is_correct_flag = True
    incorrect_hero_name = ''

    for i, argument in enumerate(arguments, 1):
        arg_split = argument.split()
        if i == len(arguments):
            if len(arg_split) > 1:
                if arg_split[-1] in SORT_BY_KEYS:
                    sort_by = arg_split[-1]
                    is_correct_flag, hero_name = find_hero_name(" ".join(arg_split[:-1]))
                    incorrect_hero_name = incorrect_hero_name if is_correct_flag else " ".join(arg_split[:-1])
                    hero_names.append(hero_name)
                else:
                    is_correct_flag, hero_name = find_hero_name(argument)
                    incorrect_hero_name = incorrect_hero_name if is_correct_flag else argument
                    hero_names.append(hero_name)
            else:
                is_correct_flag, hero_name = find_hero_name(argument)
                incorrect_hero_name = incorrect_hero_name if is_correct_flag else argument
                hero_names.append(hero_name)
        else:
            is_correct_flag, hero_name = find_hero_name(argument)
            incorrect_hero_name = incorrect_hero_name if is_correct_flag else argument
            hero_names.append(hero_name)

        if not is_correct_flag:
            break
    return is_correct_flag, hero_names, sort_by, incorrect_hero_name


def get_team_mate(message_string):
    result = ''
    example_how_to_use =   f'eg 1: `{message_string.split()[0]} axe, wr -high`\n' \
                           f'eg 2: `{message_string.split()[0]} am, oracle, zeus -med`\n' \
                           f'eg 3: `{message_string.split()[0]} timber low`\n' \
                           f'eg 4: `{message_string.split()[0]} lion, slark`'
    arguments = message_string.split()[1:]
    arguments = " ".join(arguments)
    arguments = arguments.split(',')
    is_correct_flag, hero_names, sort_by, incorrect_hero_name = extract_heroname_sortby(arguments)

    if len(hero_names) != len(set(hero_names)):
        summary = "Cannot have more than 2 hero in the same team\n" + example_how_to_use
        return is_correct_flag, summary, result

    if not is_correct_flag:
        summary = f"Could not find any hero name: **{incorrect_hero_name}**, Examples:\n" + example_how_to_use
        return is_correct_flag, summary, result

    flag, team_mate = DV.get_teammates(hero_list=hero_names, sort_by=sort_by)
    final_image = make_teammate_image(hero_names, team_mate)
    # print(hero_names, sort_by)

    return is_correct_flag, 'success', ''


if __name__ == '__main__':
    flag, summary, result = get_team_mate("!sy io, gyro, lina")
    print(flag)
    print(summary)
    print(result)
    # get_team_mate("!sy wr,  wk, am  high")
    # get_team_mate("!sy wr,  wk, am ")
    # get_team_mate("!sy wr high")
    # get_team_mate("!sy wr")
    # good, result = DV.get_teammates('!teammates wk,wr high')
