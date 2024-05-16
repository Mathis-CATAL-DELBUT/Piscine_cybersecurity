FROM debian:bullseye

EXPOSE 4242 80

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install ssh -y && \
    apt-get install openssh-server -y && \
    apt-get install nginx -y && \
    apt-get install tor -y && \
    apt-get install vim -y && \
    apt-get install sudo -y && \
    apt-get install curl -y && \
    apt-get install iptables -y


RUN echo 'root:root123' | chpasswd

COPY ./index.html /var/www/html/index.html
COPY ./nginx.conf /etc/nginx/sites-available/default
COPY ./sshd_config /etc/ssh/sshd_config
COPY ./torrc /etc/tor/torrc

CMD service ssh start && nginx -g 'daemon off;' && service tor start && tail -f /dev/null