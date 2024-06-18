
FROM debian:latest

RUN apt-get update && \
    apt-get install -y ftp && \
    apt-get install -y net-tools iproute2 iputils-ping && \
    rm -rf /var/lib/apt/lists/*

CMD tail -f /dev/null
