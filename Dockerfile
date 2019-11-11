FROM ubuntu:18.04
MAINTAINER Marshall Powell "powellmarshall3@gmail.com"

RUN apt-get update
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get install -y python3 python3-dev python3-pip build-essential nginx locales wkhtmltopdf && locale-gen en_US.UTF-8

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8


WORKDIR /home/www-data
USER www-data

COPY . /home/www-data/app
WORKDIR /home/www-data/app/backend/src

USER root
RUN  pip3 install -r requirements.txt
COPY deployment/nginx.conf /etc/nginx
RUN chmod -R 777 ../
CMD service nginx start && uwsgi --ini uwsgi.ini
