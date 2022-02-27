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
  # run one time background scrap mostly for docker build
  while :
  do
    echo "One time background scraping"
#    python3 bota/background_scrap.py -m 3
#    if [[ $? = 0 ]]; then
#        echo "**** Success ****"
#        break
#    else
#        echo "**** Restarting. One Failed **** : $?"
#    fi
    if python3 bota/background_scrap.py -m 3; then
        echo "Success"
        break
    else
        echo "Restarting, failure in scrapping "
    fi

  done
fi
