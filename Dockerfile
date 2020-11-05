FROM python:3.8-slim-buster

RUN apt-get update
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get install -y gcc
RUN apt-get install -y nginx
RUN apt-get install -y wkhtmltopdf

COPY . /app
WORKDIR /app/backend/src
RUN pip3 install -r requirements.txt
COPY deployment/nginx.conf /etc/nginx
RUN chmod -R 777 ../
EXPOSE 80
CMD service nginx start && uwsgi --ini uwsgi.ini
