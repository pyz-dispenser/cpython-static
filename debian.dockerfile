FROM debian:9.11

RUN apt-get update -y

# RUN apt-get build-dep -y python3.7
RUN apt-get install -y build-essential dpkg-dev

RUN apt-get install -y git
