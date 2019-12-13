#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
cd $BASEDIR

export DISCORD_TOKEN=$1
export DISCORD_CLIENT_ID=$2
export DOTA2_API_KEY=$3
export ADMIN_ID=$4
export TWITCH_CLIENT_IDS=$5
export LOG_PORCESS_IP_ADDRESS=$6

screen -X -S scrap quit

screen -S scrap -d -m sh run_scrap.sh
sh run_bota.sh