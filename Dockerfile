FROM python:3.11-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends tcpdump tcpreplay iproute2 traceroute nano \
 && pip install --no-cache-dir scapy \
 && apt-get clean
