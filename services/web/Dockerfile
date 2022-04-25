FROM python:3.8.1-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
# Add non-free to apt
RUN sed -i 's/main/main non-free/' /etc/apt/sources.list
RUN apt update
RUN apt install libjpeg-dev gcc zlib1g-dev p7zip-full p7zip-rar -y
RUN pip install --upgrade pip
RUN pip install wheel
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
