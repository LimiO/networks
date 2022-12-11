FROM ubuntu:20.04

WORKDIR /

RUN apt update && apt install -y iputils-ping && apt install -y python3
RUN python3 -m pip install validators

COPY . .