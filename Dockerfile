#ARG PYTHON_VERSION=3.9.1
#
#FROM python:${PYTHON_VERSION}
#
#RUN apt-get update && apt-get install -y \
#    python3-pip \
#    python3-venv \
#    python3-dev \
#    python3-setuptools \
#    python3-wheel
#
#RUN mkdir -p /app
#WORKDIR /app
#
#COPY requirements.txt .
#RUN pip install -r requirements.txt
#
#COPY . .
#
##RUN python main.py collectstatic --noinput
#
#
#EXPOSE 8080
#
## replace APP_NAME with module name
##CMD ["gunicorn", "--bind", ":8080", "--workers", "2", "demo.wsgi"]
#CMD python main.py

## pull official base image
#FROM python:3.9.6-alpine
#
## set work directory
#WORKDIR /usr/src/app
#
## set environment variables
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#
## create the app directory - and switch to it
#RUN mkdir -p /app
#WORKDIR /app
#
## install dependencies
#COPY requirements.txt /tmp/requirements.txt
#RUN set -ex && \
#    pip install --upgrade pip && \
#    pip install -r /tmp/requirements.txt && \
#    rm -rf /root/.cache/
#
## copy project
#COPY . /app/
#
## expose port 8000
#EXPOSE 8000

FROM ubuntu:20.04
RUN apt-get update && apt-get install --no-install-recommends -y python3.9 python3-pip

WORKDIR /s1te
COPY requirements.txt /s1te/
RUN pip install -r requirements.txt
COPY . /s1te/
CMD ["gunicorn", "--bind", ":8000", "--workers", "1", "s1te.wsgi:application"]
#CMD python3 main.py
