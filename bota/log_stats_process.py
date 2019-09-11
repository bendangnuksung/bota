import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
# import datetime
from datetime import datetime
import calendar
from bota import constant


def findDay(date):
    born = datetime.strptime(date, '%Y-%m-%d').weekday()
    return (calendar.day_name[born])


class LogStat():
    def __init__(self, file_path=constant.COMMAND_USER_LOG_PATH):
        self.log_file_path = file_path
        self.new_user_dict = {}
        self.new_server_dict = {}
        self.update_df()

    def update_df(self):
        self.df = self.log_to_df(self.log_file_path)

    def update_new_user_and_server(self, user_id, server_id, date_time):
        try:
            date = datetime.date(date_time)
            if user_id in self.new_user_dict:
                saved_date = self.new_user_dict[user_id]
                if saved_date > date:
                    self.new_user_dict[user_id] = date
            else:
                self.new_user_dict[user_id] = date

            if server_id in self.new_server_dict:
                saved_date = self.new_server_dict[server_id]
                if saved_date > date:
                    self.new_server_dict[server_id] = date
            else:
                self.new_server_dict[server_id] = date

        except Exception as e:
            pass
        return

    def log_to_df(self, file):
        with open(file) as f:
            raw_string = f.readlines()
            prepared = []
            for line in raw_string:
                try:
                    date_time, data = line.split('INFO')
                    uname, uid, is_server, sid, sname, channel, total_members, command_called, nsfw, command_passed = data.split(
                        ',')
                except Exception as e:
                    uname, uid, is_server, sid, sname, channel, total_members, command_called, nsfw = data.split(',')[:9]
                    command_passed = ','.join(data.split(',')[9:])

                date_time_format = datetime.strptime(date_time.strip(),"%Y-%m-%d %H:%M:%S")
                date = datetime.date(date_time_format)
                time = datetime.time(date_time_format)
                hour = time.replace(microsecond=0,second=0,minute=0)
                self.update_new_user_and_server(uid, sid, date_time_format)
                command_passed = command_passed.replace('\n', '')
                weekday = findDay(date_time.split()[0])
                is_weekend = True if weekday in ['Saturday', 'Sunday'] else False
                prepared.append([date_time.strip(), uname.strip(), uid.strip(), is_server, sid.strip(), sname.strip(),
                                 channel.strip(), total_members.strip(), command_called.strip(), nsfw.strip(),
                                 command_passed.strip(), weekday, is_weekend, date, hour])

        df = pd.DataFrame(prepared)
        df.columns = ['date_time', 'user', 'user_id', 'is_server', 'server_id', 'server_name', 'channel', 'total_members',
                      'command_called', 'nsfw', 'command_passed', 'weekday', 'weekend', 'date', 'hour']
        df['date_time'] = df['date_time'].astype('datetime64[ns]')
        return df

    def get_most_activate_user(self, top):
        df = self.df
        most_active = df.groupby("user")["command_called"].count().sort_values()
        p = pd.DataFrame(most_active)
        p = p.iloc[-(top):]
        return p

    def make_new_user_and_server_df(self):
        # New user df
        user_ids = list(self.new_user_dict.keys())
        user_join_date = list(self.new_user_dict.values())
        col_names = ['user_id', 'join_date']
        new_user_df = pd.DataFrame(columns=col_names)
        new_user_df['user_id'] = user_ids
        new_user_df['join_date'] = user_join_date

        # New server df
        server_ids = list(self.new_server_dict.keys())
        server_join_date = list(self.new_server_dict.values())
        col_names = ['server_id', 'join_date']
        new_server_df = pd.DataFrame(columns=col_names)
        new_server_df['server_id'] = server_ids
        new_server_df['join_date'] = server_join_date

        return new_user_df, new_server_df

    def get_new_user_and_server(self, tail=True, n=7):
        new_user_df, new_server_df = self.make_new_user_and_server_df()
        group_new_user_by_dates = new_user_df.groupby("join_date")["user_id"].count()
        group_new_server_by_dates = new_server_df.groupby("join_date")["server_id"].count()
        if tail:
            new_user_series = group_new_user_by_dates.tail(n)
            new_server_series = group_new_server_by_dates.tail(n)
        else:
            new_user_series = group_new_user_by_dates.head(n)
            new_server_series = group_new_server_by_dates.head(n)
        combined = pd.concat([new_user_series, new_server_series], axis=1)
        ax = combined.plot.bar(figsize=(12, 6))
        for p in ax.patches:
            ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
        path = os.path.join(constant.TEMP_IMAGE_PATH, 'new_user_server.jpg')
        plt.savefig(path)
        plt.close()
        plt.clf()

    def get_command_calls(self, n=7):
        calls = self.df.groupby("date")["date"].count()
        calls = calls.tail(n)
        ax = calls.plot.bar()
        for p in ax.patches:
            ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
        path = os.path.join(constant.TEMP_IMAGE_PATH, 'command_calls.jpg')
        plt.savefig(path)
        plt.close()
        plt.clf()


if __name__ == '__main__':
    logstat = LogStat('/home/ben/Downloads/bota_log.txt')
    # logstat.get_new_user_and_server(n=10)
    logstat.get_command_calls()
