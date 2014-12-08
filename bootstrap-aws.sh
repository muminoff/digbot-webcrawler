#!/bin/bash

set -e

sudo apt-get install build-essential libssl-dev libffi-dev python-dev python-setuptools libpq-dev libxslt-dev -y
sudo easy_install pip
sudo pip install -r /app/requirements.txt
scrapy crawl digspider
