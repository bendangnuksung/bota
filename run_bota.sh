#!/usr/bin/env bash

echo "Please make sure this is running in Screen or any type of background session"

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

python3 bota/main.py
python3 notify_message.py -m 1