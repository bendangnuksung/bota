from bota.utility.db_utility import BotaDB
from bota import db_constants as dbc
from bota.constant import DEFAULT_PREFIX


bota_db = BotaDB(host=dbc.HOST_NAME, database=dbc.DATABASE_NAME,
                     user=dbc.USER, password=dbc.PASSWORD)


class GuildCaller:
    def __init__(self):
        pass

    def get_guild_settings(self, guild_id):
        columns = [dbc.COLUMN_GUILD_PREFIX, dbc.COLUMN_GUILD_BLOCK_CHANNEL]
        wherekey = {dbc.COLUMN_GUILD_ID: guild_id}
        try:
            r = bota_db.select_query(dbc.TABLE_GUILD, columns, wherekey)[0]
        except:
            r = [None, None]
        return r

    def guild_exist(self, guild_id):
        wherekey = {dbc.COLUMN_GUILD_ID: guild_id}
        r = bota_db.select_query(dbc.TABLE_GUILD, [dbc.COLUMN_GUILD_ID], wherekey)
        if len(r) == 0:
            return False
        return True

    def _get_prefix_from_db(self, guild_id):
        flag = True
        wherekey = {dbc.COLUMN_GUILD_ID: guild_id}
        r = bota_db.select_query(dbc.TABLE_GUILD, [dbc.COLUMN_GUILD_PREFIX], wherekey)
        if len(r) == 0:
            prefix = DEFAULT_PREFIX
            flag = False
        else:
            prefix = r[0][0]
        return flag, prefix

    def add_guild(self, guild_id, guild_name):
        value = {dbc.COLUMN_GUILD_ID: guild_id, dbc.COLUMN_GUILD_NAME: guild_name,
                 dbc.COLUMN_GUILD_PREFIX: DEFAULT_PREFIX, dbc.COLUMN_GUILD_BLOCK_CHANNEL: []}
        bota_db.write_single(dbc.TABLE_GUILD, value)

    def get_prefix(self, guild_id, guild_name):
        flag, prefix = self._get_prefix_from_db(guild_id)
        if not flag:
            self.add_guild(guild_id, guild_name)
        return prefix

    def get_block_channel_names(self, guild_id):
        wherekey = {dbc.COLUMN_GUILD_ID: guild_id}
        try:
            r = bota_db.select_query(dbc.TABLE_GUILD, [dbc.COLUMN_GUILD_BLOCK_CHANNEL], wherekey)[0][0]
        except Exception as e:
            print('BLock channels: ', e)
            r = []
        return r

    def update_prefix(self, guild_id, prefix):
        if not self.guild_exist(guild_id):
            return False
        wherekey = {dbc.COLUMN_GUILD_ID: guild_id}
        value = {dbc.COLUMN_GUILD_PREFIX: prefix}
        bota_db.update_single(dbc.TABLE_GUILD, value, wherekey)
        return True

    def delete_channel_from_blocklist(self, guild_id, channel_name):
        if not self.guild_exist(guild_id):
            return False
        channel_name = channel_name.lower().strip()
        # get block channels list first
        wherekey = {dbc.COLUMN_GUILD_ID: guild_id}
        block_channels = bota_db.select_query(dbc.TABLE_GUILD, [dbc.COLUMN_GUILD_BLOCK_CHANNEL], wherekey)[0][0]
        new_block_channels = []
        for channel in block_channels:
            if channel == channel_name or channel is None or channel == []:
                continue
            new_block_channels.append(channel)

        # update block list
        if len(new_block_channels) > 0:
            value = {dbc.COLUMN_GUILD_BLOCK_CHANNEL: new_block_channels}
            bota_db.update_single(dbc.TABLE_GUILD, value, wherekey)

        else:
            value = {dbc.COLUMN_GUILD_BLOCK_CHANNEL: []}
            bota_db.update_single(dbc.TABLE_GUILD, value, wherekey)

        return True

    def add_channel_to_blocklist(self, guild_id, channel_name):
        if not self.guild_exist(guild_id):
            return False
        channel_name = channel_name.lower().strip()
        # get block channels list first
        wherekey = {dbc.COLUMN_GUILD_ID: guild_id}
        block_channels = bota_db.select_query(dbc.TABLE_GUILD, [dbc.COLUMN_GUILD_BLOCK_CHANNEL], wherekey)[0][0]
        print('block channel: ', block_channels)
        block_channels.append(channel_name)
        block_channels = list(set(block_channels))

        value = {dbc.COLUMN_GUILD_BLOCK_CHANNEL: block_channels}
        bota_db.update_single(dbc.TABLE_GUILD, value, wherekey)

        return True


if __name__ == '__main__':
    guild = GuildCaller()
    gid = '2'
    print(guild.get_guild_settings('10'))
    print(guild.get_prefix(gid, 'test'))
    print("done")
    # print(guild.add_channel_to_blocklist(gid, 'testing1'))
    print(guild.delete_channel_from_blocklist(gid, 'testing2'))
    print(guild.get_block_channel_names('5'))

