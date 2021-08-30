from python:3.7.7

RUN git clone https://github.com/bendangnuksung/bota.git

# Apt setup
RUN apt-get update && \
    pip install --upgrade pip && \
    apt install -y libgl1-mesa-glx && \
    apt-get install -y screen

RUN git clone https://github.com/joshuaduffy/dota2api.git && \
    cd dota2api && \
    python setup.py install && \
    cd ../ && \
    rm -rf dota2api


## webscreenshot
RUN apt-get install -y xvfb && \
    apt-get install -y phantomjs


## firefox
RUN apt-get install -y software-properties-common
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A6DCF7707EBC211F
RUN apt-add-repository "deb http://ppa.launchpad.net/ubuntu-mozilla-security/ppa/ubuntu bionic main"
RUN apt-get update && \
    apt-get install -y firefox

# Gecko Driver
ENV GECKODRIVER_VERSION 0.29.1
RUN wget --no-verbose -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v$GECKODRIVER_VERSION/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz \
  && rm -rf /opt/geckodriver \
  && tar -C /opt -zxf /tmp/geckodriver.tar.gz \
  && rm /tmp/geckodriver.tar.gz \
  && mv /opt/geckodriver /opt/geckodriver-$GECKODRIVER_VERSION \
  && chmod 755 /opt/geckodriver-$GECKODRIVER_VERSION \
  && ln -fs /opt/geckodriver-$GECKODRIVER_VERSION /usr/bin/geckodriver \
  && ln -fs /opt/geckodriver-$GECKODRIVER_VERSION /usr/bin/wires


# install chromium
RUN apt-get install -y chromium && \
    curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

ENTRYPOINT ./bota/run_bota_docker.sh

RUN cd bota/ && \
    git pull
RUN pip install -r bota/requirements.txt
# make Directories
RUN mkdir -p bota/bota/data/steam_user
RUN mkdir -p bota/bota/data/counter_heroes
RUN mkdir -p bota/bota/data/good_against_heroes
RUN mkdir -p bota/bota/data/guide_build
RUN mkdir -p bota/bota/data/items_build


# run scrap during building
RUN cd bota/ && \
    export PYTHONPATH=$PYTHONPATH:$pwd && \
    sh run_scrap.sh 3

# sudo docker build --network host -f dockerfile -t DOCKERNAME:TAGNAME .
# 
