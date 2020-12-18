from python:3.7.7

RUN git clone https://github.com/bendangnuksung/bota.git

# make Directories
RUN mkdir bota/bota/data/counter_heroes bota/bota/data/good_against_heroes
RUN mkdir bota/bota/data/guide_build bota/bota/data/items_build bota/bota/data/steam_user bota/bota/data/temp_images bota/bota/data/logs


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


## Run once time update:
RUN cd /bota && \
    sh run_scrap.sh 3


ENTRYPOINT /bota/run_bota_docker.sh

