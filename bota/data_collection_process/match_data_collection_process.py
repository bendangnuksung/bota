import json
import requests
import os
from tqdm import tqdm
from datetime import date, datetime
import logging
from bota.utility.general import make_dir_if_not_exist
from bota.private_constant import DOTA2_API_KEY
from bota.data_collection_process.fetch_data_from_api import fetch_and_save_match_ids
from bota.constant import RAW_MATCH_JSON_DATA_PATH, MATCH_TEMP_PROCESS_LOG, PROCESSED_MATCH_DATA_PATH, \
    WRITE_TEMP_LOG_AFTER_BATCH, WRITE_JSON_AFTER_BATCH, UPDATE_THREHSHOLD_FOR_MATCH_ID, SKILL_BRACKET


make_dir_if_not_exist(RAW_MATCH_JSON_DATA_PATH)
make_dir_if_not_exist(os.path.dirname(MATCH_TEMP_PROCESS_LOG))
make_dir_if_not_exist(PROCESSED_MATCH_DATA_PATH)


formatter = logging.Formatter('%(message)s')


def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


def make_hero_dict_list(end=129):
    hero_dict = {}
    for i in range(1, end+1):
        hero_dict[i] = {}
        for j in range(1, end+1):
            if i == j:
                continue
            hero_dict[i][j] = {'win': 0, 'loss': 0}
    return hero_dict


def get_last_log_line(path=MATCH_TEMP_PROCESS_LOG):
    try:
        file = open(path)
        for line in reversed(file.readlines()):
            line = line.split(',')
            return line
    except Exception:
        return ''


def extract_heroes_from_steam_api(match_id, api_key=DOTA2_API_KEY, timeout=5):
    url = f'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?match_id={match_id}&key={api_key}'
    data = None
    try:
        r = requests.get(url, timeout=timeout)
        data = r.json()
    except Exception as e:
        print(e)
        return None, None
    players = data['result']['players']

    won_heroes = []
    loss_heroes = []
    radiant_win = data['result']['radiant_win']
    for i, player in enumerate(players):
        hero_id = player['hero_id']
        if i < 5:
            if radiant_win:
                won_heroes.append(hero_id)
            else:
                loss_heroes.append(hero_id)
        else:
            if not radiant_win:
                won_heroes.append(hero_id)
            else:
                loss_heroes.append(hero_id)
    return won_heroes, loss_heroes


def extract_heroes_from_opendota_api(match_id, timeout=5):
    url = f'https://api.opendota.com/api/matches/{match_id}'
    data = None
    try:
        r = requests.get(url, timeout=timeout)
        data = r.json()
    except Exception as e:
        print(e)
        return None, None
    players = data['players']

    won_heroes = []
    loss_heroes = []
    for i, player in enumerate(players):
        hero_id = player['hero_id']
        if player['win']:
            won_heroes.append(hero_id)
        else:
            loss_heroes.append(hero_id)

    return won_heroes, loss_heroes


def get_won_loss_heroes(n, match_id):
    won_heroes, loss_heroes = None, None
    flag = True
    if n % 2 == 0:
        try:
            won_heroes, loss_heroes = extract_heroes_from_opendota_api(match_id)
        except:
            try:
                won_heroes, loss_heroes = extract_heroes_from_steam_api(match_id)
            except Exception:
                flag = False
    else:
        try:
            won_heroes, loss_heroes = extract_heroes_from_steam_api(match_id)
        except:
            try:
                won_heroes, loss_heroes = extract_heroes_from_opendota_api(match_id)
            except Exception:
                flag = False
    return flag, won_heroes, loss_heroes


def extract_match_details():
    fetch_and_save_match_ids()
    files = os.listdir(RAW_MATCH_JSON_DATA_PATH)
    match_id_json = [os.path.join(RAW_MATCH_JSON_DATA_PATH, file) for file in files if file.endswith(".json")]

    match_id_json = sorted(match_id_json)

    for file_index, m_json in enumerate(match_id_json):
        with open(m_json) as f:
            json_data = json.load(f)
            json_data = json_data['rows']

        log_last_line = get_last_log_line()
        log_index = 0

        print("")
        print("*" * 70)
        print(f"{os.path.basename(m_json)}:")
        print("*" * 70)

        if log_last_line != '':
            last_time_stamp = log_last_line[0]
            last_time_stamp = datetime.strptime(last_time_stamp, '%Y-%m-%d %H:%M:%S.%f').timestamp()
            current_time_stamp = datetime.now().timestamp()
            if (current_time_stamp - last_time_stamp) < UPDATE_THREHSHOLD_FOR_MATCH_ID:
                log_file_index = log_last_line[1]
                if file_index < int(log_file_index):
                    print("Already Completed! Process Next.")
                    continue
                if file_index == int(log_file_index):
                    log_index = int(log_last_line[3])

        today = date.today()
        today_date = today.strftime("%d-%m-%Y")
        processed_file_path = os.path.join(PROCESSED_MATCH_DATA_PATH, today_date + '_' + os.path.basename(m_json))
        processed_csv_path = os.path.join(PROCESSED_MATCH_DATA_PATH, today_date + '_' +
                                          os.path.basename(m_json).replace('json', 'csv'))
        command_logger = setup_logger('command_logger', processed_csv_path)

        hero_dict = make_hero_dict_list()
        if os.path.exists(processed_file_path) and log_index < 0:
            hero_dict = json.load(processed_file_path)

        iterator = tqdm(range(len(json_data)))
        for i in iterator:
            if i < log_index:
                continue
            row = json_data[i]
            match_id = row['match_id']
            # url = MATCH_URL + str(match_id)
            flag, won_heroes, loss_heroes = get_won_loss_heroes(i, match_id)
            if not flag:
                print("Skipped")
                continue

            for w_hero in won_heroes:
                for l_hero in loss_heroes:
                    hero_dict[w_hero][l_hero]['win'] += 1
                    hero_dict[l_hero][w_hero]['loss'] += 1
            current_time = datetime.now()
            won_heroes = [str(hero) for hero in won_heroes]
            loss_heroes = [str(hero) for hero in loss_heroes]
            csv_hero_log = f"{current_time},{match_id},{','.join(won_heroes)},{','.join(loss_heroes)}"
            command_logger.info(csv_hero_log)

            if i % WRITE_JSON_AFTER_BATCH == 0:
                with open(processed_file_path, 'w') as f:
                    json.dump(hero_dict, f)

            if i % WRITE_TEMP_LOG_AFTER_BATCH == 0:
                temp_log = f'{current_time},{file_index},{os.path.basename(m_json)},{i}'
                with open(MATCH_TEMP_PROCESS_LOG, 'w') as f:
                    f.write(temp_log)

            # print(i)
            # if i > 100:
            #     iterator.close()
            #     break


if __name__ == '__main__':
    extract_match_details()
