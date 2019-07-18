#!/usr/bin/env bash

cd /dotabot/
pip3 install -r requirements.txt
python3 -m pip install -U discord.py

wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
tar xf  wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
cd wkhtmltox/bin/
mv wkhtmltopdf  /usr/bin/wkhtmltopdf
mv wkhtmltoimage  /usr/bin/wkhtmltoimage
cd ../../
rm -rf wkhtmltox*

git clone https://github.com/joshuaduffy/dota2api.git`
cd dota2api
python setup.py install
cd ../
rm -rf dota2api

