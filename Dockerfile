FROM ubuntu:14.04
MAINTAINER Sardor Muminov <smuminov@gmail.com>
RUN apt-get update -y \
&& apt-get install build-essential libssl-dev libffi-dev python-dev python-setuptools libpq-dev libxslt-dev -y
RUN apt-get install redis-server -y
ADD . /app
RUN easy_install pip
RUN pip install -r /app/requirements.txt
RUN /etc/init.d/redis-server start
RUN cd /app && scrapy crawl digspider
