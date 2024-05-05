FROM debian:bullseye

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install ssh -y && \
    apt-get install openssh-server -y && \
    apt-get install nginx -y && \
    apt-get install tor -y && \
    apt-get install vim -y && \
    apt-get install sudo -y

CMD service ssh start && service nginx start && service tor start && tail -f /dev/null