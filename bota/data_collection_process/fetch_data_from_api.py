import requests
import json
import os
from bota.utility.general import is_file_old

from bota.constant import SKILL_BRACKET, LIMIT, OPENDOTA_URL, RANK_ID, GET_PUBLIC_MATCH_TIMEOUT, ATTRS_WANTED,\
    RAW_MATCH_JSON_DATA_PATH, UPDATE_THREHSHOLD_FOR_MATCH_ID


def fetch_and_save_match_ids(limit=LIMIT):
    files = os.listdir(RAW_MATCH_JSON_DATA_PATH)
    match_id_json = [os.path.join(RAW_MATCH_JSON_DATA_PATH, file) for file in files if file.endswith(".json")]

    if len(match_id_json) >= len(SKILL_BRACKET):
        flag = False
        for file_path in match_id_json:
            if is_file_old(file_path, UPDATE_THREHSHOLD_FOR_MATCH_ID):
                flag = True
        if not flag:
            print(f"Files are less older than {(UPDATE_THREHSHOLD_FOR_MATCH_ID //86400)} days\n"
                  f"Hence Skipping of getting Match IDs")
            return

    for skill_bracket in SKILL_BRACKET:
        starting_mmr = SKILL_BRACKET[skill_bracket]['start_mmr']
        ending_mmr = SKILL_BRACKET[skill_bracket]['end_mmr']
        query = f'select {", ".join(ATTRS_WANTED)} from public_matches where num_mmr > 0 and lobby_type = {RANK_ID}' \
                f' and avg_mmr > {starting_mmr} and avg_mmr < {ending_mmr} order by start_time desc limit {limit}'
        url = OPENDOTA_URL + query
        url = url.encode()

        r = requests.get(url, timeout=GET_PUBLIC_MATCH_TIMEOUT)
        data = r.json()
        path_to_save = os.path.join(RAW_MATCH_JSON_DATA_PATH, skill_bracket + '.json')
        print("*"*50)
        print(f"Dumping {skill_bracket} json data to {path_to_save}")
        with open(path_to_save, 'w') as f:
            json.dump(data, f)


if __name__ == "__main__":
    fetch_and_save_match_ids()
