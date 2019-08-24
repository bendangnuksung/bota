from bota.utility.db_utility import BotaDB
from bota import db_constants as dbc
import requests
from bota import constant


class UserDB():

    def __init__(self):
        self.bota_db = BotaDB()

    def is_steam_id_valid(self, steam_id):
        steam_id = str(steam_id)
        url = constant.PLAYER_URL_BASE + steam_id
        r = requests.get(url,  headers={'user-agent': 'Mozilla/5.0'})
        print(r.status_code)
        if r.status_code == 200:
            return True
        return False

    def is_discord_id_exist(self, discord_id):
        r = self.bota_db.is_unique_key_exist(dbc.TABLE_USER_INFO, dbc.COLUMN_DISCORD_ID, int(discord_id))
        return r

    def _check_conditions(self, discord_id, steam_id):
        flag = True
        reason = ''

        if not self.is_steam_id_valid(steam_id):
            reason = f'**{steam_id}** STEAM ID is not valid'
            flag = False

        try:
            int(discord_id)
            int(steam_id)
        except Exception:
            reason = 'Not proper STEAM ID'
            flag = False

        return flag, reason

    def add_user(self, discord_id, discord_name, steam_id, language="en"):
        flag, reason = self._check_conditions(discord_id, steam_id)
        if not flag:
            return flag, reason
        discord_id, steam_id = int(discord_id), int(steam_id)
        final_dictionary = {dbc.COLUMN_DISCORD_ID: discord_id, dbc.COLUMN_DISCORD_NAME: discord_name,
                            dbc.COLUMN_STEAM_ID: steam_id, dbc.COLUMN_LANGUAGE: language}
        self.bota_db.write_single(dbc.TABLE_USER_INFO, final_dictionary)
        return flag, 'Steam ID was successfully added'

    def update_steam_id(self, discord_id, steam_id):
        flag, reason = self._check_conditions(discord_id, steam_id)
        if not flag:
            return flag, reason
        if not self.is_discord_id_exist(discord_id):
            return False, "Your Profile has not been saved yet."

        discord_id, steam_id = int(discord_id), int(steam_id)
        where_key = {dbc.COLUMN_DISCORD_ID: discord_id}
        final_dictionary = {dbc.COLUMN_STEAM_ID: steam_id}
        self.bota_db.update_single(dbc.TABLE_USER_INFO, final_dictionary, where_key=where_key)
        return flag, 'Steam ID was successfully updated'

    def get_steam_id(self, discord_id):
        discord_id = int(discord_id)
        where_key = {dbc.COLUMN_DISCORD_ID: discord_id}
        column_wanted = [dbc.COLUMN_STEAM_ID]
        result = self.bota_db.select_query(dbc.TABLE_USER_INFO, column_wanted, where_key)
        if not len(result):
            return '', 'Please Save your Steam ID first'
        return result[0][0], 'Successful'


class AliasDB():
    def __init__(self):
        self.bota_db = BotaDB()

    def is_steam_id_valid(self, steam_id):
        steam_id = str(steam_id)
        url = constant.PLAYER_URL_BASE + steam_id
        r = requests.get(url,  headers={'user-agent': 'Mozilla/5.0'})
        if r.status_code == 200:
            return True
        return False

    def is_alias_name_exist(self, alias_name):
        alias_name = "'" + alias_name + "'"
        r = self.bota_db.is_unique_key_exist(dbc.TABLE_ALIAS, dbc.COLUMN_ALIAS_NAME, alias_name)
        return r

    def _check_conditions(self, alias_name, discord_id, steam_id):
        flag = True
        reason = ''

        if not self.is_steam_id_valid(steam_id):
            reason = f'**{steam_id}** STEAM ID is not valid'
            flag = False

        try:
            test = int(alias_name)
            reason = f'Alias should be contain alphabets'
            flag = False
        except Exception:
            pass

        try:
            int(discord_id)
            int(steam_id)
        except Exception:
            reason = 'Not proper STEAM ID'
            flag = False

        return flag, reason

    def get_discord_id(self, alias_name):
        where_key = {dbc.COLUMN_ALIAS_NAME: alias_name}
        column_wanted = [dbc.COLUMN_DISCORD_ID]
        result = self.bota_db.select_query(dbc.TABLE_ALIAS, column_wanted, where_key)
        if not len(result):
            return '', 'Please Save your Steam ID first'
        return result[0][0], 'Successful'

    def add_alias_name(self, alias_name, discord_id, steam_id):
        flag, reason = self._check_conditions(alias_name, discord_id, steam_id)
        if not flag:
            return flag, reason
        discord_id, steam_id = int(discord_id), int(steam_id)
        final_dictionary = {dbc.COLUMN_ALIAS_NAME: alias_name, dbc.COLUMN_DISCORD_ID: discord_id, dbc.COLUMN_STEAM_ID: steam_id}
        self.bota_db.write_single(dbc.TABLE_ALIAS, final_dictionary)
        return flag, f'**{alias_name}** has been successfully added. Type:   **`!profile {alias_name}`**'

    def update_steam_id(self, alias_name, discord_id, steam_id):
        flag, reason = self._check_conditions(alias_name, discord_id, steam_id)
        if not flag:
            return flag, reason
        discord_id, steam_id = int(discord_id), int(steam_id)

        if not self.is_alias_name_exist(alias_name):
            return False, f"**{alias_name}** does not exist"

        saved_discord_id, _ = self.get_discord_id(alias_name)
        if saved_discord_id != discord_id:
            return False, f"**{alias_name}** has already been taken by someone else, Use another name"

        where_key = {dbc.COLUMN_ALIAS_NAME: alias_name}
        final_dictionary = {dbc.COLUMN_STEAM_ID: steam_id}
        self.bota_db.update_single(dbc.TABLE_ALIAS, final_dictionary, where_key=where_key)
        return flag, f'Steam ID succesfully updated for **{alias_name}**, Type:   **`!profile {alias_name}`**'

    def get_steam_id(self, alias_name):
        where_key = {dbc.COLUMN_ALIAS_NAME: alias_name}
        column_wanted = [dbc.COLUMN_STEAM_ID]
        result = self.bota_db.select_query(dbc.TABLE_ALIAS, column_wanted, where_key)
        if not len(result):
            return '', 'Please Save your Steam ID first'
        return result[0][0], 'Successful'


if __name__ == '__main__':
    # user = UserDB()
    # print(user.add_user('111111111', 'test1', '111620041'))
    # print(user.get_steam_id('111111111'))
    # print(user.update_steam_id('123456789', '111620041'))

    alias = AliasDB()
    # print(alias.add_user('dav', '123456789', '123456789'))
    # print(alias.update_steam_id('dav', '123456789', '11111111'))
    print(alias.get_steam_id('bad'))