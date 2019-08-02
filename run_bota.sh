#!/usr/bin/env bash

# Set PYTHONPATH to current working directory
wrk= pwd
export PYTHONPATH=PYTHONPATH:$wrk

# Stop if it is running already
screen -X -S bota quit
screen -X -S scrap quit

# Run process
screen -S bota -d -m python3 bota/main.py
screen -S scrap -d -m python3 bota/background_scrap.py
echo "Running main.py, background_scrap.py in background"
echo "Type 'screen -r bota' to check bota process"
echo "Tyoe 'screen -r scrap' to check background process"

echo "To stop both the process, run: 'stop_bota.sh'"