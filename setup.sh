#!/usr/bin/env bash

echo "making directory"
cd bota/data/
mkdir background character_icons character_icons_big counter_heroes good_against_heroes
mkdir guide_build items items_build medals steam_user temp_images logs
cd ../../

sudo apt-get update
sudo apt-get install libfontconfig1 libxrender1
sudo apt-get install libjpeg-dev zlib1g-dev
sudo apt-get install screen

echo "Installing requirements.txt"
pip3 install -r requirements.txt

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
python3 setup.py install
cd ../
rm -rf dota2api
