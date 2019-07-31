#!/usr/bin/env bash

# Stop if it is running already
screen -X -S bota quit
screen -X -S scrap quit

# Run process
screen -S bota -d -m python3 main.py
screen -S scrap -d -m python3 background_scrap.py
echo "Running main.py, background_scrap.py in background"
echo "Type 'screen -r' to check process"
echo "To stop both the process, run: 'stop_bota.sh'"