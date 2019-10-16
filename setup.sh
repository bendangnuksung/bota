#!/usr/bin/env bash

echo "making directory"
cd bota/data/
mkdir background character_icons character_icons_big counter_heroes good_against_heroes
mkdir guide_build items items_build medals steam_user temp_images logs
cd ../../

sudo apt-get update
sudo apt-get install python3-pip
pip3 install -U "urllib3<1.25"
sudo apt-get install libfontconfig1 libxrender1
sudo apt-get install libjpeg-dev zlib1g-dev
sudo apt-get install screen

echo "Installing requirements.txt"
pip3 install -r requirements.txt
pip3 uninstall opencv-python
sudo apt install python3-opencv

echo "Installing  Rapptz/Discord "
python3 -m pip install -U discord.py
cd discord.py
sudo pip3 install -r requirements.txt
python3 setup.py install
cd ..
rm -rf discord.py

echo "Setting Up wkhtmltox......"
wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
tar xf  wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
cd wkhtmltox/bin/
sudo mv wkhtmltopdf  /usr/bin/wkhtmltopdf
sudo mv wkhtmltoimage  /usr/bin/wkhtmltoimage
cd ../../
rm -rf wkhtmltox*

echo "Joshuaduffy Dota2api setup...."
git clone https://github.com/joshuaduffy/dota2api.git
cd dota2api
sudo python3 setup.py install
cd ../
sudo rm -rf dota2api

echo "Pyppeteer dependencies installation...."
sudo apt-get update && sudo apt-get install -yq --no-install-recommends libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 libnss3 