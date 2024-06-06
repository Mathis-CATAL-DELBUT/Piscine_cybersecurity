FROM debian:latest

RUN useradd -m -s /bin/bash mcatal-d
USER mcatal-d

WORKDIR /home/mcatal-d

RUN mkdir infection

COPY ./dist/stockholm .
COPY test* ./infection/

CMD tail -f /dev/null