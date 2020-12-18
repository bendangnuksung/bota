#!/usr/bin/env bash

cd /bota

git pull origin master
export DISCORD_TOKEN=$1
export DISCORD_CLIENT_ID=$2
export DOTA2_API_KEY=$3
export ADMIN_ID=$4
export TWITCH_CLIENT_IDS=$5
export TWITCH_SECRET_KEY=$6
export LOG_PORCESS_IP_ADDRESS=$7

screen -X -S scrap quit

screen -S scrap -d -m sh run_scrap.sh

while true
do
  git pull origin master
  sh run_bota.sh
done