FROM python:3.8.1-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt update
RUN apt install libjpeg-dev gcc zlib1g-dev p7zip-full -y
RUN pip install --upgrade pip
RUN pip install wheel
COPY ./p7zip-rar_16.02-3_amd64.deb /usr/src/app/p7zip-rar_16.02-3_amd64.deb
RUN apt install ./p7zip-rar_16.02-3_amd64.deb
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
