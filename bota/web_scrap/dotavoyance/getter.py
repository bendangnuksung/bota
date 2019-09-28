from bota.web_scrap.dotavoyance.dotavoyance import Dotavoyance
from bota.web_scrap.heroes_process import find_hero_name
from bota.image_processing import add_border_to_image, write_text_pil
import cv2
import os
from bota import constant
from bota.help import TEAM_CMD_EXAMPLE

DV = Dotavoyance()
SORT_BY_KEYS = ['high', 'med', 'low', 'highest', 'higher', 'normal', 'medium', 'norm', 'mid', 'top', 'bot', 'lowerst',
                'lower', 'middle']
SORT_BY_ALT_KEYS = {'highest': 'high', 'higher': 'high', 'normal': 'med', 'medium': 'med', 'norm': 'norm',
                    'mid': 'med', 'top': 'high', 'bot': 'low', 'lowest': 'low', 'lower': 'low', 'middle': 'med'}
SKILL_DICT = {'high': 'High Skill', 'med': 'Normal Skill', 'low': 'Low Skill', '': 'All Skill'}
HERO_COUNT_MIN_GAMES = {1: 100, 2: 50, 3: 5, 4: 2}


def display(img):
    import matplotlib.pyplot as plt
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.show()


def extract_heroname_and_sortby(arguments):
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

    if sort_by in SORT_BY_ALT_KEYS:
        sort_by = SORT_BY_ALT_KEYS[sort_by]

    return is_correct_flag, hero_names, sort_by, incorrect_hero_name


def make_teammate_image(my_heroes, results, skill_level, bg_image=constant.DV_TEAM_BG_IMAGE):
    bg_image = cv2.imread(bg_image)
    bg_h, bg_w, _ = bg_image.shape
    start_left = 50
    start_top = 170

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
                hero_icon_y = start_left + 700
            else:
                hero_icon_x = start_top + (((k+1) // 2) * 90)
                hero_icon_y = start_left
            bg_image[hero_icon_x: hero_icon_x + icon_h, hero_icon_y: hero_icon_y + icon_w, :] = hero_icon

            win_rate_x = hero_icon_x + (icon_h // 3)
            win_rate_y = hero_icon_y + (icon_w // 2) + 275
            percen = str(result['win_percentage']) + '%'
            pos = (win_rate_y, win_rate_x)
            bg_image = write_text_pil(bg_image, percen, pos, size=40)
            count += 1
    bg_image = write_text_pil(bg_image, skill_level, ((bg_image.shape[1]//2) - 70, (bg_image.shape[0]//2)-50), size=45)

    return bg_image


def make_teammate_image_without_percentage(my_heroes, results, skill_level, bg_image=constant.DV_TEAM_BG_IMAGE_WITHOUT_WINRATE):
    bg_image = cv2.imread(bg_image)
    bg_h, bg_w, _ = bg_image.shape

    my_hero_start_top = 675
    my_hero_start_left = ((bg_w // 2) - 85) - (((len(my_heroes) -1) * 200) // 2)
    for i, hero_name in enumerate(my_heroes):
        hero_icon = cv2.imread(os.path.join(constant.ICON_PATH_BIG, hero_name + '.png'))
        hero_icon = add_border_to_image(hero_icon)
        icon_h, icon_w, _ = hero_icon.shape
        hero_icon_x = my_hero_start_top
        hero_icon_y = my_hero_start_left + (i * 200)
        bg_image[hero_icon_x: hero_icon_x + icon_h, hero_icon_y: hero_icon_y + icon_w, :] = hero_icon

    start_left = 160
    start_top = 270

    for i, result in enumerate(results):
        hero_names = result['heroes']
        for j, hero_name in enumerate(hero_names):
            image = cv2.imread(os.path.join(constant.ICON_PATH_BIG, hero_name + '.png'))
            image = cv2.resize(image, (int(constant.COUNTER_ICON_SHAPE[1]*1.5), int(constant.COUNTER_ICON_SHAPE[0]*1.5)))
            image = add_border_to_image(image)
            x, y = start_top, start_left
            x = x + ((i // constant.COUNTER_MAX_COLUMN) * 150)
            y = y + ((i % constant.COUNTER_MAX_COLUMN) * image.shape[1]) + \
                ((i % constant.COUNTER_MAX_COLUMN) * constant.COUNTER_WIDTH_DIST)
            bg_image[x: x + image.shape[0], y: y + image.shape[1], :] = image
            break
    bg_image = write_text_pil(bg_image, skill_level, ((bg_image.shape[1]//2) - 70, start_top - 100), size=45)

    return bg_image


def get_team_mate(message_string):
    result = ''
    arguments = message_string.split()[1:]
    arguments = " ".join(arguments)
    arguments = arguments.split(',')
    is_correct_flag, hero_names, sort_by, incorrect_hero_name = extract_heroname_and_sortby(arguments)

    if len(hero_names) != len(set(hero_names)):
        summary = "Cannot have more than 2 same hero in the team\n" + TEAM_CMD_EXAMPLE
        return is_correct_flag, summary, result, []

    if not is_correct_flag and len(message_string.split()) == 1:
        summary = f"Please provide a  hero name: \n" + TEAM_CMD_EXAMPLE
        return is_correct_flag, summary, result, []

    if not is_correct_flag:
        summary = f"Could not find any hero name: **{incorrect_hero_name}**\n" + TEAM_CMD_EXAMPLE
        return is_correct_flag, summary, result, []

    min_games = HERO_COUNT_MIN_GAMES[len(hero_names)]
    flag, team_mate_raw = DV.get_teammates(hero_list=hero_names, sort_by=sort_by, min_games=min_games)
    team_mate = []
    for t in team_mate_raw:
        if t['win_percentage'] != 100:
            team_mate.append(t)

    # sort_by = DV.get_sort_col(sort_by)
    file_name = "_".join(sorted(hero_names)) + '-' + sort_by + '.jpg'
    file_path = os.path.join(constant.DV_TEAM_IMAGE_PATH, file_name)

    if not flag:
        if len(hero_names) > 3:
            summary = f"Sorry! Could not find any results. Please try with **{len(hero_names) - 1}** Hero Names"
            return False, summary, result, []
        else:
            summary = f"Sorry! Could not find any results. Please try with other Hero Names"
            return False, summary, result, []

    skill_level = SKILL_DICT[sort_by]
    final_image = make_teammate_image_without_percentage(hero_names, team_mate, skill_level)
    cv2.imwrite(file_path, final_image)
    summary = f'eg 1: **`!sy lion, am high`**\n' \
              f'eg 2: **`!sy lion, am normal`**\n'
    return is_correct_flag, summary, file_path, hero_names


if __name__ == '__main__':
    flag, summary, image_path, hero_names = get_team_mate("!sy drow, luna, aa, bm")
    print(flag, summary, image_path)
    # get_team_mate("!sy wr,  wk, am  high")
    # get_team_mate("!sy wr,  wk, am ")
    # get_team_mate("!sy wr high")
    # get_team_mate("!sy wr")
    # good, result = DV.get_teammates('!teammates wk,wr high')
