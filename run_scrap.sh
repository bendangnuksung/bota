# Set PYTHONPATH to current working directory
export PYTHONPATH=PYTHONPATH:$pwd

if [ -z "$1" ]
  then
    while true
    do
      echo "mode 2"
      python3 bota/background_scrap.py -m 2
      echo "sleeping for 120 seconds"
      sleep 120
    done
else
  python3 bota/background_scrap.py -m 3
fi
