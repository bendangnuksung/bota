# Set PYTHONPATH to current working directory
export PYTHONPATH=PYTHONPATH:$pwd

if [ -z "$1" ]
  then
    while true
    do
      python3 bota/background_scrap.py -m 2
      sleep 30
    done
else
  python3 bota/background_scrap.py -m 3
fi

