FROM debian:bullseye

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install vim -y && \
    apt-get install python3 -y && \
    apt-get install pip -y && \
    pip install cryptography && \
    apt-get install sudo -y


RUN mkdir /home/infection

COPY ./stockholm.py /home/infection
COPY ./stockholm.txt /home/infection

CMD tail -f /dev/null