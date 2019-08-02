#!/usr/bin/env bash

# Set PYTHONPATH to current working directory
wrk= pwd
export PYTHONPATH=PYTHONPATH:$wrk

# Check if all wanted private keys exist in bota/private_constant.py
if python3 check_keys.py 2>&1 >/dev/null; then
    echo 'All private key are present'
else
    python3 check_keys.py
    echo 'exiting ....'
    exit 1
fi

# Stop if it is running already
screen -X -S bota quit
screen -X -S scrap quit

# Run process
screen -S bota -d -m python3 bota/main.py
screen -S scrap -d -m python3 bota/background_scrap.py -m 2
echo "Running main.py, background_scrap.py in background"
echo "Type 'screen -r bota' to check bota process"
echo "Tyoe 'screen -r scrap' to check background process"

echo "To stop both the process, run: 'stop_bota.sh'"