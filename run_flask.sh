#!/usr/bin/env bash

# Set Python Path
export PYTHONPATH=$PYTHONPATH:$pwd

# Run flask server
while true
do
  python3 flask_process/flask_main.py
done