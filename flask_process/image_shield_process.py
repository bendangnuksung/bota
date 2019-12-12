from datetime import datetime
import os


class BotaLog():
    def __init__(self, file_path):
        self.file_path = file_path
        self.n_servers = "Null"
        self.n_users = "Null"
        self.last_time_update = "Null"
        self._load_last_update_file()

    def _load_last_update_file(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                line = f.readlines()[0]
                line = line.split(',')
                if len(line) > 2:
                    self.n_servers = line[0]
                    self.n_users = line[1]
                    self.last_time_update = line[2]

    def write_to_last_update_file(self):
        with open(self.file_path, "w") as f:
            text = ",".join([self.n_servers, self.n_users, self.last_time_update])
            f.write(text)

    def update_info(self, n_servers, n_users):
        self.n_servers = n_servers
        self.n_users = n_users
        self.last_time_update = str(datetime.now())
        self.write_to_last_update_file()

    def get_info(self):
        return {'n_servers': self.n_servers, 'n_users': self.n_users, 'last_time_update': self.last_time_update}

