from flask import jsonify
from flask import Flask, request
from flask_process.image_shield_process import BotaLog
from flask_process.logs_constant import IMAGE_SHIELD_JSON_FILE
from flask_process.flask_log_process import save_command_logs, get_command_log_tail
from flask_process.flask_log_stat_process import LogStat
import base64
import gc
import sys

botalog = BotaLog(IMAGE_SHIELD_JSON_FILE)
logstat = LogStat()
app = Flask(__name__)


def check_enough_memory(min_free_mb_ram=10):
    file = open('/proc/meminfo')
    lines = file.readlines()
    for line in lines:
        if 'MemFree' in line:
            attrs = line.split()
            value = int(attrs[1])
            value = value / 1000
            if value > min_free_mb_ram:
                file.close()
                return True
            file.close()
            return False
    file.close()
    return True


@app.route('/updatestat', methods=['POST'])
def updatestat():
    n_servers = request.form.get('guilds')
    n_users = request.form.get('users')
    botalog.update_info(n_servers, n_users)
    return jsonify({'result': True})


@app.route('/getstat')
def getstat():
    stat = botalog.get_info()
    gc.collect()
    return jsonify(stat)


@app.route('/stats/update_command_log', methods=['POST'])
def update_command_log():
    log = request.form.get('log')
    save_command_logs(log)
    gc.collect()

    # If not enough RAM restart the server
    # (Running the flask service in Shell script in a while loop)
    if not check_enough_memory():
        sys.exit()

    return jsonify({'result': True})


@app.route('/stats/all_time', methods=['POST'])
def get_stats_all_time():
    text_dict = logstat.all_time()
    gc.collect()
    return jsonify(text_dict)


@app.route('/stats/new_user_and_server', methods=['POST'])
def get_stats_new_user_and_server():
    n = request.form.get('n')
    n = int(n)
    img_path, summary = logstat.get_new_user_and_server(n=n)
    data = {'summary': summary}
    with open(img_path, mode='rb') as file:
        img = file.read()
    data['image'] = base64.encodebytes(img).decode("utf-8")
    gc.collect()
    return jsonify(data)


@app.route('/stats/command', methods=['POST'])
def get_stats_command():
    n = request.form.get('n')
    n = int(n)
    img_path, summary = logstat.get_commands_stats(n=n)
    data = {'summary': summary}
    with open(img_path, mode='rb') as file:
        img_1 = file.read()
    data['image'] = base64.encodebytes(img_1).decode("utf-8")
    gc.collect()
    return jsonify(data)


@app.route('/stats/calls', methods=['POST'])
def get_stats_calls():
    n = request.form.get('n')
    n = int(n)
    img_path, summary = logstat.get_command_calls(n=n)
    data = {'summary': summary}
    with open(img_path, mode='rb') as file:
        img_1 = file.read()
    data['image'] = base64.encodebytes(img_1).decode("utf-8")
    gc.collect()
    return jsonify(data)


@app.route('/stats/update', methods=['POST'])
def stats_update():
    if not check_enough_memory():
        sys.exit()
    flag = logstat.update_df()
    # update_value_to_server(logstat, force_update=True)
    data = {'flag': flag}
    gc.collect()
    return jsonify(data)


@app.route('/stats/tail', methods=['POST'])
def get_tail():
    n = request.form.get('n')
    n = int(n)
    tail_data = get_command_log_tail(n)
    data = {'tail': tail_data}
    gc.collect()
    return jsonify(data)


app.run(host='0.0.0.0', port=5000)
