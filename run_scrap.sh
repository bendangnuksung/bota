# Set PYTHONPATH to current working directory
wrk= pwd
export PYTHONPATH=PYTHONPATH:$wrk

while true:
do
  python3 bota/background_scrap.py -m 2
  python3 notify_message -m 2
  sleep 5
done

