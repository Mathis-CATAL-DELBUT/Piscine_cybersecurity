FROM debian:latest

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y vsftpd && \
    apt-get install -y vim && \
    apt-get install -y net-tools iproute2 iputils-ping && \
    rm -rf /var/lib/apt/lists/* 

RUN    mkdir -p /var/run/vsftpd/empty
RUN    chown root:root /var/run/vsftpd/empty

RUN useradd -m ftpuser && \
    echo "ftpuser:password" | chpasswd

COPY vsftpd.conf /etc/vsftpd.conf

EXPOSE 21 40000-40009

CMD ["/usr/sbin/vsftpd", "/etc/vsftpd.conf"]