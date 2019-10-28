# Check https://hub.docker.com/_/debian?tab=tags for the latest
FROM debian:stable-20191014

RUN apt-get update -y

# RUN apt-get build-dep -y python3.7
RUN apt-get install -y build-essential dpkg-dev
RUN apt-get install -y libreadline-dev

RUN apt-get install -y git
