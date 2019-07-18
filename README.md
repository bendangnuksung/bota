# Discord DOTA Bot


### Installation
* Discord.py Installation (1.0.0)
    1. git clone -b rewrite https://github.com/Rapptz/discord.py.git
    2. cd discord.py
    3. sudo pip3 install -r requirements.txt
    4. python3 setup.py install
    5. cd ..
    6. rm -rf discord.py
* Install Requirements
    1. wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
    2. tar xf  wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
    3. cd wkhtmltox/bin/
    4. mv wkhtmltopdf  /usr/bin/wkhtmltopdf 
    5. sudo mv wkhtmltoimage  /usr/bin/wkhtmltoimage
    6. git clone https://github.com/joshuaduffy/dota2api.git
$ cd dota2api
$ python setup.py install
