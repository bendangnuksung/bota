from python:3.7.7

RUN git clone https://github.com/bendangnuksung/bota.git

# make Directories
RUN mkdir bota/bota/data/steam_user

# Apt setup
RUN apt-get update && \
    pip install --upgrade pip && \
    apt install -y libgl1-mesa-glx && \
    apt-get install -y screen


# installing package
RUN pip install -r bota/requirements.txt


RUN git clone https://github.com/joshuaduffy/dota2api.git && \
    cd dota2api && \
    python setup.py install && \
    cd ../ && \
    rm -rf dota2api


## webscreenshot
RUN apt-get install -y xvfb && \
    apt-get install -y phantomjs

# install chromium
RUN apt-get install -y chromium

RUN cd bota/ && \
    git pull && \
    export PYTHONPATH=$PYTHONPATH:$pwd && \
    python bota/background_scrap.py --mode 3


ENTRYPOINT ./bota/run_bota_docker.sh


# sudo docker build --network host -f dockerfile -t DOCKERNAME:TAGNAME .
# 
