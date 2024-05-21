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

RUN echo 'root:root' | chpasswd
RUN useradd mathis && echo 'mathis:test' | chpasswd

RUN mkdir -p /home/mathis/.ssh && chown mathis:mathis /home/mathis/.ssh && chmod 700 /home/mathis/.ssh

COPY ./bonus/mathis_key.pub /home/mathis/.ssh/authorized_keys
RUN chown mathis:mathis /home/mathis/.ssh/authorized_keys && chmod 600 /home/mathis/.ssh/authorized_keys

# COPY ./index.html /var/www/html/index.html
COPY ./bonus /var/www/html

COPY ./nginx.conf /etc/nginx/sites-available/default

# COPY ./sshd_config /etc/ssh/sshd_config
COPY ./bonus/sshd_config /etc/ssh/sshd_config


COPY ./torrc /etc/tor/torrc

CMD service ssh start && \
    nginx && \
    su debian-tor -s /bin/bash -c "tor"
