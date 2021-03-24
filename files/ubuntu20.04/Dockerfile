FROM ubuntu:20.04

MAINTAINER Tanu Malik <tanu.malik@depaul.edu>

RUN apt-get update && apt-get install -y cmake && \
    apt-get clean

RUN apt-get update & apt-get install -y software-properties-common && \
    apt-get clean

#RUN apt-get update && apt-get install -y python3.7 && \
#    apt-get clean

RUN apt-get update && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get clean

RUN apt-get update && apt-get -y install python3.7 && \
    apt-get clean

RUN apt-get update && apt-get install -y python3-pip && \
    apt-get clean

RUN python3.7 -m pip install --upgrade pip

RUN apt-get update && apt-get install -y tzdata && \
    apt-get clean

RUN apt-get update && apt-get install -y git && \
    apt-get clean
