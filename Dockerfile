FROM python:3.8-slim-buster as base
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get install -y gcc wkhtmltopdf git
RUN apt-get install -y nginx
COPY deployment/nginx.conf /etc/nginx

# option 1. local development (doesnt pull from github)
#COPY . /app

# option 2. pull from github
RUN git clone https://github.com/powellm4/mindbody-payroll.git /app

RUN chmod -R 777 /app

WORKDIR /app/backend/src
RUN pip3 install -r requirements.txt

##### Start new image: Debug
FROM base as debug
EXPOSE 5000
RUN pip install debugpy
CMD python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m flask --debug run -h 0.0.0.0 -p 5000

#### Start new image: production
FROM base as prod
EXPOSE 80
CMD service nginx start && uwsgi --ini uwsgi.ini
