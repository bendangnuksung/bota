import json
import os
from bota.constant import STEAM_USER_FILE_PATH
from bota import constant
import requests
import csv

# Saving Users in Json atm, if user base grows will jump to SQL


class User():
    def __init__(self, file_path=STEAM_USER_FILE_PATH, new_user_csv_path=constant.NEW_USER_FILE_PATH_CSV):
        self.max_n_user = 2000000 # 2 Million max users
        self.file_path = file_path
        self.new_user_csv_path = new_user_csv_path
        self._load_users()
        self._merge_new_user()

    def _write_json(self, dictionary):
        with open(self.file_path, 'w') as fp:
            json.dump(dictionary, fp)

    def _merge_new_user(self):
        if not os.path.isfile(self.new_user_csv_path):
            return
        new_user_dict = {}
        with open(self.new_user_csv_path, 'r') as f:
            reader = csv.reader(f)
            for line in reader:
                new_user_dict[line[0].strip()] = line[1].strip()
        self.user_info.update(new_user_dict)
        self._write_json(self.user_info)
        os.remove(self.new_user_csv_path)

    def _append_csv(self, key, value):
        with open(self.new_user_csv_path, 'a') as fp:
            fp.write(f"{key}, {value}\n")

    def _load_users(self):
        if not os.path.isfile(self.file_path):
            data = {}
            self._write_json(data)

        with open(STEAM_USER_FILE_PATH) as f:
            self.user_info = json.loads(f.read())

    def is_id_valid(self, id):
        url = constant.PLAYER_URL_BASE + id
        r = requests.get(url,  headers={'user-agent': 'Mozilla/5.0'})
        print(url)
        print(r.status_code)
        if r.status_code == 200:
            return True
        return False

    def _check_conditions(self, user_name, id):
        flag = True
        reason = ''
        if len(self.user_info) > self.max_n_user:
            reason = 'Sorry, reached maximum user limit. Will upgrade server soon :)'
            flag = False

        if not self.is_id_valid(id):
            reason = f'{id} ID is not valid'
            flag = False

        if user_name in self.user_info:
            reason = f'{user_name} is already taken'
            flag = False

        try:
            test = int(user_name)
            reason = f'Alias should be contain alphabets'
            flag = False
        except Exception:
            pass

        return flag, reason

    def add_user(self, user_name, id):
        flag, reason = self._check_conditions(user_name, id)
        if not flag:
            return flag, reason

        self.user_info[user_name] = int(id)
        self._append_csv(user_name, int(id))
        return flag, 'successful'

    def get_id(self, user_name):
        if user_name not in self.user_info:
            return False, ''
        return True, str(self.user_info[user_name])


if __name__ == '__main__':
    user = User()
    print(user.user_info)
    flag, reason = user.add_user('ben', '86753879')
    print(flag, reason)
    print(user.user_info)
    flag, user_name = user.get_id('ben')
    print(flag, user_name)