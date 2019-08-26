import psycopg2
from bota import db_constants as dbc
import psycopg2.extras
import json


class BotaDB:
    def __init__(self, host=dbc.HOST_NAME, database=dbc.DATABASE_NAME, user=dbc.USER, password=dbc.PASSWORD):
        self.credentials_empty, self.credentials_empty_list = self._is_db_credentials_empty(host, database, user, password)
        if self.credentials_empty:
            print(f"DB credentials empty, \n{self.credentials_empty_list}")
        else:
            self._connect_and_get_cursor(host, database, user, password)

    def _is_db_credentials_empty(self, host, database, user, password):
        credentials_empty_list = []
        flag = False
        if host == '':
            credentials_empty_list.append('host')
            flag = True
        if database == '':
            credentials_empty_list.append('database')
            flag = True
        if user == '':
            credentials_empty_list.append('user')
            flag = True
        if password == '':
            credentials_empty_list.append('password')
            flag = True
        return flag, credentials_empty_list

    def _connect_and_get_cursor(self, host, database, user, password):
        self.conn = psycopg2.connect(host=host, database=database, user=user, password=password)
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.cursor.execute('SELECT version()')

    def execute(self, query, values=None):
        try:
            final_value = []
            for value in values:
                if type(value) == dict:
                    final_value.append(json.dumps(value))
                else:
                    final_value.append(value)
            self.cursor.execute(query, final_value)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print('ERROR:', error)

        try:
            return self.cursor.fetchall()
        except Exception:
            print("Cursor fetch: None")
            return None

    def is_unique_key_exist(self, table_name, column_name, column_value):
        self.cursor.execute(f"SELECT {column_name} FROM {table_name} WHERE {column_name} = {column_value}")
        return self.cursor.fetchone() is not None

    def make_write_query(self, table_name, dictionary):
        head = f'INSERT INTO {table_name} '
        column_name = []
        column_placeholder = []
        column_value = []
        for key, value in dictionary.items():
            column_name.append(key)
            column_placeholder.append("%s")
            column_value.append(value)
        column_name = "(" + ",".join(column_name) + ")"
        column_placeholder = "(" + ",".join(column_placeholder) + ")"

        final_query = head + column_name + " VALUES " + column_placeholder
        return final_query, tuple(column_value)

    def make_update_query(self, table_name, dictionary, where_key):
        head = f'UPDATE {table_name} '
        column_name = []
        where_name = []
        column_values = []

        for key, value in dictionary.items():
            column_name.append(key + '=(%s)')
            column_values.append(value)

        for key, value in where_key.items():
            where_name.append(key + '=(%s)')
            column_values.append(value)

        column_name = ", ".join(column_name)
        where_name = "and".join(where_name)

        final_query = f"{head} SET  {column_name} WHERE {where_name}"
        return final_query, tuple(column_values)

    def make_select_query(self, table_name, column_names, where_key):
        head = f'select '
        where_name = []
        column_values = []
        for key, value in where_key.items():
            where_name.append(key + '=(%s)')
            column_values.append(value)

        column_name = ", ".join(column_names)
        where_name = "and".join(where_name)

        final_query = f"{head} {column_name} from {table_name} WHERE {where_name}"
        return final_query, tuple(column_values)

    def write_single(self, table_name, dictionary):
        """
        :param table_name: (str) name of the table
        :param dictionary: (dictionaries) {COLUMN_NAME_1: VAL_1, COLUMN_NAME_2: VAL_2}
                         eg: {user_id: 123456789, user_name: abcdef}
        :return:
        """
        query, value = self.make_write_query(table_name, dictionary)
        self.execute(query, value)

    def update_single(self, table_name, dictionary, where_key):
        """
        :param table_name: (str) name of the table
        :param dictionary: (dictionaries) {COLUMN_NAME_1: VAL_1, COLUMN_NAME_2: VAL_2}
                         eg: {user_id: 123456789, user_name: abcdef}
        :param where_key: (dictionaries) {COLUMN_NAME_1: VAL_1}
        :return:
        """
        query, value = self.make_update_query(table_name,  dictionary, where_key)
        self.execute(query, value)

    def select_query(self, table_name, column_names, where_key):
        """
        :param table_name: (str) name of table
        :param column_names: (list) list of column names
        :param where_key: (dictionaries) {COLUMN_NAME_1: VAL_1}
        :return: (list of list) returns row values of columns requested
        """
        query, value = self.make_select_query(table_name, column_names, where_key)
        result = self.execute(query, value)
        return result


if __name__ == '__main__':
    bota_db = BotaDB(host=dbc.HOST_NAME, database=dbc.DATABASE_NAME,
                     user=dbc.USER, password=dbc.PASSWORD)

    # # Write DB
    # value = {dbc.COLUMN_USER_ID: 123456789, dbc.COLUMN_USER_NAME: 'dav#5585',
    #          dbc.COLUMN_STEAM_ID: 297066030, dbc.COLUMN_LANGUAGE: 'en', dbc.COLUMN_OTHERS: {1:2}}
    # bota_db.write_single(dbc.TABLE_USER_INFO, value)

    # UPDATE DB
    # where_key = {dbc.COLUMN_USER_ID: 470624487331594244}
    # value = {dbc.COLUMN_LANGUAGE: 'ru'}
    # bota_db.update_single(dbc.TABLE_USER_INFO, value, where_key)

    # Select DB
    value = [dbc.COLUMN_STEAM_ID, dbc.COLUMN_DISCORD_NAME, dbc.COLUMN_LANGUAGE, dbc.COLUMN_OTHERS]
    where_key = {dbc.COLUMN_DISCORD_ID: 4706244873315942445}
    r = bota_db.select_query(dbc.TABLE_USER_INFO, value, where_key)
    print(r)

    # Key exist
    # print(bota_db.is_unique_key_exist(dbc.TABLE_USER_INFO, dbc.COLUMN_DISCORD_ID, 123456789))
