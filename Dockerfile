FROM python:2.7
MAINTAINER Sardor Muminov <smuminov@gmail.com>
RUN mkdir /spider
ADD requirements.txt /spider
WORKDIR /spider
RUN pip install -r requirements.txt
ADD . /spider
