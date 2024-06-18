FROM debian:latest

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y vim python3 python3-pip python3-venv && \
    apt-get install -y ftp && \
    apt-get install -y tcpdump net-tools iproute2 && \
    apt-get install -y net-tools iproute2 iputils-ping && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /home/inquisitor/venv && \
    /home/inquisitor/venv/bin/pip install libpcap && \
    /home/inquisitor/venv/bin/pip install scapy 
    # /home/inquisitor/venv/bin/pip install pcapy

# source /home/inquisitor/venv/bin/activate 

COPY inquisitor.py /home/inquisitor/inquisitor.py

CMD tail -f /dev/null
