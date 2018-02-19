FROM python:3.4-slim

USER root

# Setup and install base system software

RUN echo "locales locales/locales_to_be_generated multiselect en_US.UTF-8 UTF-8" | debconf-set-selections \
    && echo "locales locales/default_environment_locale select en_US.UTF-8" | debconf-set-selections \
    && apt-get update \
    && apt-get --yes --no-install-recommends install \
        locales tzdata ca-certificates sudo \
        bash-completion iproute2 curl nano tree
ENV LANG en_US.UTF-8

# Apt packages for face_recognition

RUN apt-get install --yes --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
&& apt-get clean && rm -rf /tmp/* /var/tmp/*

# User creation start

RUN addgroup \
        --quiet \
        --gid 1000 \
        dockuser \
    && adduser \
        --quiet \
        --home /home/dockuser \
        --uid 1000 \
        --ingroup dockuser \
        --disabled-password \
        --shell /bin/bash \
        --gecos 'Python 3' \
        dockuser \
    && usermod \
        --append \
        --groups sudo \
        dockuser \
    && echo 'dockuser ALL=NOPASSWD: ALL' > /etc/sudoers.d/dockuser

# Python environment configuration start

ENV PYTHONUNBUFFERED 1

RUN mkdir /home/dockuser/code
WORKDIR /home/dockuser/code
ADD requirements.txt /home/dockuser/code/
RUN pip install -r requirements.txt
ADD . /home/dockuser/code/

EXPOSE 8000

USER dockuser
