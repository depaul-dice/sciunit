FROM ubuntu:16.04

MAINTAINER Zhihao Yuan <tanu.malik@depaul.edu>

RUN apt-get update && apt-get install -y cmake && \
    apt-get clean

RUN apt-get update & apt-get install -y software-properties-common && \
    apt-get clean

RUN apt-get update && add-apt-repository ppa:deadsnakes/ppa && \
    apt-get clean

RUN apt-get update && apt-get install -y python3.6 && \
    apt-get clean

RUN update-alternatives --install /usr/bin/python3 python3 \
    /usr/bin/python3.6 1

RUN apt-get update && apt-get install -y python3-pip && \
    apt-get clean

RUN pip3 install --upgrade pip

RUN apt-get update && apt-get install -y git && \
    apt-get clean
