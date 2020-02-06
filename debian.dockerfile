# Check https://hub.docker.com/_/debian?tab=tags for the latest
FROM debian:stable-20200130

RUN apt-get update -y

# RUN apt-get build-dep -y python3.7
# From https://salsa.debian.org/cpython-team/python3/blob/master/debian/control
RUN apt-get install -y build-essential dpkg-dev
RUN apt-get install -y libreadline-dev libreadline-dev libncursesw5-dev>=5.3 \
    zlib1g-dev libbz2-dev liblzma-dev libgdbm-dev libdb-dev tk-dev blt-dev>=2.4z \
    libssl-dev libexpat1-dev libmpdec-dev>=2.4 locales-all libsqlite3-dev \
    libffi-dev>=3.0.5
    # libbluetooth-dev libgpm2

RUN apt-get install -y git
