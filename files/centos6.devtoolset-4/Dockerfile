FROM centos:centos6.6

MAINTAINER Zhihao Yuan <zhihao.yuan@depaul.edu>

RUN yum install -y --setopt=tsflags=nodocs centos-release-scl && \
    yum clean all

RUN yum install -y --setopt=tsflags=nodocs devtoolset-4-gcc-c++ && \
    yum clean all

RUN yum install -y --setopt=tsflags=nodocs epel-release && \
    yum clean all

RUN yum install -y --setopt=tsflags=nodocs cmake3 && \
    yum clean all

RUN ln -s /usr/bin/cmake3 /usr/bin/cmake

RUN yum install -y --setopt=tsflags=nodocs python27-python-devel && \
    yum clean all

RUN yum install -y --setopt=tsflags=nodocs git && \
    yum clean all

RUN yum install -y --setopt=tsflags=nodocs tar && \
    yum clean all

RUN echo 'source scl_source enable devtoolset-4 python27' >> ~/.bashrc
