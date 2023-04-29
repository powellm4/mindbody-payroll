FROM python:3.8-slim-buster as base

RUN apt-get update
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get install -y gcc
RUN apt-get install -y wkhtmltopdf

COPY . /app
WORKDIR /app/backend/src
RUN pip3 install -r requirements.txt
RUN chmod -R 777 ../

##### Start new image: Debug
FROM base as debug
EXPOSE 5000
RUN pip install debugpy
CMD python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m flask --debug run -h 0.0.0.0 -p 5000

#### Start new image: production
FROM base as prod
RUN apt-get install -y nginx
COPY deployment/nginx.conf /etc/nginx
EXPOSE 80
CMD service nginx start && uwsgi --ini uwsgi.ini

