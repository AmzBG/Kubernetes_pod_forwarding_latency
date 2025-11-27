FROM amzbg/scapy-image:2

RUN apt update -y && apt upgrade -y && apt-get install tcpdump -y ; apt-get install tcpreplay -y ; apt clean

WORKDIR /app

COPY script.py /app/pod.py

CMD [ "python" ,"/app/pod.py"]