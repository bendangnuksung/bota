import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta
import calendar
# from bota import constant
from flask_process import logs_constant
import re
import gc


def findDay(date):
    born = datetime.strptime(date, '%Y-%m-%d').weekday()
    return (calendar.day_name[born])


class LogStat():
    def __init__(self, file_path=logs_constant.LOG_PATH, client=None):
        self.log_file_path = file_path
        self.new_user_dict = {}
        self.new_server_dict = {}
        self.client = client
        self.last_update_line_number = 0
        self.df = []
        self.update_df()
        self.commands = ['!top game', '!trend', '!reddit', '!protrack', '!counter', '!item', '!good', '!skill',
                         '!twitch', '!profile']

    def update_df(self):
        if os.path.exists(self.log_file_path):
            # del self.df # deleting for memory reason
            if self.last_update_line_number == 0:
                self.df = self.log_to_df(self.log_file_path)
            else:
                new_df = self.log_to_df(self.log_file_path)
                if type(new_df) != list:
                    frames = [self.df, new_df]
                    del self.df
                    self.df = pd.concat(frames)
            gc.collect()
            return True
        else:
            print("*"*80)
            print(f"LOG FILE: {self.log_file_path} does not exist")
            print("*" * 80)
            return False

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
            if len(raw_string) == 0:
                return []
            prepared = []
            raw_string = raw_string[self.last_update_line_number: ]
            if len(raw_string) == 0:
                return []
            for line in raw_string:
                try:
                    date_time, data = line.split('INFO')
                    uname, uid, is_server, sid, sname, channel, total_members, command_called, nsfw, command_passed = data.split(
                        ',')
                except Exception as e:
                    uname, uid, is_server, sid, sname, channel, total_members, command_called, nsfw = data.split(',')[:9]
                    command_passed = ','.join(data.split(',')[9:])
                self.last_update_line_number += 1
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

    def get_most_activate_user(self, top, alltime=True, days=7):
        df = self.df
        most_active = df.groupby("user")["command_called"].count().sort_values()
        p = pd.DataFrame(most_active)
        p = p.iloc[-(top):]
        return p

    def get_most_active_group(self, top, alltime=True, days=7):
        df = self.df
        most_active = df.groupby("server_name")["command_called"].count().sort_values()
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
        summary = f"New Users and Servers in last {n} days"
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
        path = os.path.join(logs_constant.NEW_USER_SERVER_IMAGE_PATH)
        plt.savefig(path)
        plt.close()
        plt.clf()
        return logs_constant.NEW_USER_SERVER_IMAGE_PATH, summary

    def get_command_calls(self, n=7):
        summary = f"Commands & Unique User calls in last {n} days"
        date_calls = self.df.groupby("date")["date"].count()
        date_calls = date_calls.tail(n)
        temp_dates = date_calls.index._ndarray_values
        temp_rows = []
        for temp_date in temp_dates:
            temp_ids = self.df[self.df['date'] == temp_date]
            temp_ids_count = temp_ids.groupby("user_id")["user_id"].size().shape[0]
            temp_rows.append(temp_ids_count)

        unique_user_calls_ondate = pd.Series(temp_rows, index=temp_dates)

        date_calls = date_calls.rename("Total Calls")
        unique_user_calls_ondate = unique_user_calls_ondate.rename("Unique User Call")

        combined = pd.concat([date_calls, unique_user_calls_ondate], axis=1)
        ax = combined.plot.bar(figsize=(12, 7), color=[(0.5,0.4,0.5), (0.75, 0.75, 0.25)]*5)
        for p in ax.patches:
            ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
        path = os.path.join(logs_constant.COMMAND_CALLS_IMAGE_PATH)
        plt.savefig(path)
        plt.close()
        plt.clf()
        return logs_constant.COMMAND_CALLS_IMAGE_PATH, summary

    def get_active_group(self, n=10):
        pass

    def get_commands_stats(self, n=7):
        summary = f"Command call stats in last {n} days"
        date_calls = self.df.groupby("date")["date"].count()
        date_calls = date_calls.tail(n)
        temp_dates = date_calls.index._ndarray_values

        temp_rows = {}
        for command in self.commands:
            temp_rows[command] = []

        for i, temp_date in enumerate(temp_dates):
            temp_ids = self.df[self.df['date'] == temp_date]
            command_called_group = temp_ids.groupby("command_called")["command_called"].count().to_dict()

            for key, value in command_called_group.items():
                if key == '':
                    continue
                for cmd_name in self.commands:
                    if key in cmd_name:
                        temp_rows[cmd_name].append(value)
                        break
            for key in temp_rows:
                if len(temp_rows[key]) < (i + 1):
                    temp_rows[key].append(0)

        calls = []
        for command_name in temp_rows:
            temp_pd = pd.Series(temp_rows[command_name], index=temp_dates)
            name = re.sub("[^a-zA-Z ]", '', command_name)
            temp_pd = temp_pd.rename(name)
            calls.append(temp_pd)

        combined = pd.concat(calls, axis=1)
        ax = combined.plot.bar(figsize=(11, 30), rot=0, subplots=True)
        ax[1].legend(loc=2)
        path = os.path.join(logs_constant.COMMAND_STATS_IMAGE_PATH)

        plt.savefig(path)
        plt.close()
        plt.clf()
        return logs_constant.COMMAND_STATS_IMAGE_PATH, summary

    def _get_call_count_from_date(self, start, end):
        mask = (self.df['date'] > start) & (self.df['date'] <= end)
        return self.df.loc[mask].shape[0]

    def all_time(self):
        total_calls = self.df.shape[0]
        if self.client is not None:
            total_guilds = len(list(self.client.guilds))
        else:
            total_guilds = self.df.groupby('server_id')['server_id'].count().shape[0]
        total_users = self.df.groupby('user_id')['user_id'].count().shape[0]

        current_week_start = date.today() - timedelta(days=8)
        current_week_end = date.today() - timedelta(days=1)
        last_week_start = date.today() - timedelta(days=16)
        last_week_end = date.today() - timedelta(days=9)

        current_total_week_calls = self._get_call_count_from_date(current_week_start, current_week_end)
        last_total_week_calls = self._get_call_count_from_date(last_week_start, last_week_end)
        last_total_week_calls = last_total_week_calls if last_total_week_calls > 0 else 1

        change_in_percen = ((current_total_week_calls / last_total_week_calls) - 1) * 100
        change_in_percen = str(round(change_in_percen, 2)) + "%"
        change_in_percen = change_in_percen if '-' in change_in_percen else '+' + change_in_percen

        return {'Total Calls': total_calls, 'Total Guilds': total_guilds, 'Total Users': total_users,
                'Last Week Calls': str(last_total_week_calls), 'Current Week Calls': str(current_total_week_calls),
                'Percentage Change': change_in_percen}


if __name__ == '__main__':
    import psutil
    logstat = LogStat('/Users/ben/personal/bota/flask_process/logs/command_logs.txt')
    for i in range(5):
        if i != 0:
            logstat.update_df()
        logstat.get_commands_stats()
        logstat.get_command_calls(30)
        logstat.get_new_user_and_server(n=21)
        process = psutil.Process(os.getpid())
        print(process.memory_info().rss)
        print(logstat.all_time())
        # print(logstat.get_most_activate_user(50))
