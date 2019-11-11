FROM ubuntu:18.10
MAINTAINER Marshall Powell "powellmarshall3@gmail.com"

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip build-essential nginx


WORKDIR /home/www-data
USER www-data

COPY . /home/www-data/app
WORKDIR /home/www-data/app/backend/src

USER root
RUN  pip3 install -r requirements.txt
COPY deployment/nginx.conf /etc/nginx

CMD service nginx start && uwsgi --ini uwsgi.ini
