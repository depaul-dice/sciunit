FROM ubuntu:18.04

MAINTAINER Zhihao Yuan <tanu.malik@depaul.edu>

RUN apt-get update && apt-get install -y cmake && \
    apt-get clean

RUN apt-get update & apt-get install -y software-properties-common && \
    apt-get clean

RUN apt-get update && apt-get install -y python3.6 && \
    apt-get clean

RUN apt-get update && apt-get install -y python3-pip && \
    apt-get clean

RUN pip3 install --upgrade pip

RUN apt-get update && apt-get install -y git && \
    apt-get clean
