#!/usr/bin/env bash

export DISCORD_TOKEN=$1
export DISCORD_CLIENT_ID=$2
export DOTA2_API_KEY=$3
export ADMIN_ID=$4
export TWITCH_CLIENT_IDS=$5
export LOG_PORCESS_IP_ADDRESS=$6

screen -X -S bota quit
screen -X -S scrap quit

screen -S bota -d -m sh run_scrap.sh
sh run_bota.sh