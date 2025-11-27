import matplotlib.pyplot as plt
from sre_constants import SUCCESS
from scapy.all import *
import time,os


def get_data_from_pkt(p):
    try:
        #print(bytes(p[TCP].payload))
        return bytes(p[TCP].payload)
    except:
            return b''

def get_timestamp_from_pkt(p):
    return p.time

def read_pcap(file):
    return rdpcap(file)

def find_packet_in_pcap(pkt,pkt_load):
    for x in pkt_load:
        if get_data_from_pkt(pkt)==get_data_from_pkt(x):
            return get_timestamp_from_pkt(x)-get_timestamp_from_pkt(pkt) - 35
    return -1


def analyze():
    counter=-1
    plot_data=[[],[]]
    size=0
    data_sender=read_pcap('src.pcap')
    data_receiver=read_pcap('target.pcap')
    success=0
    t=get_timestamp_from_pkt(data_receiver[-1])-get_timestamp_from_pkt(data_sender[0])
    
    for x in data_sender:
        latency=find_packet_in_pcap(x,data_receiver) - sum(plot_data[1])
        counter+=1
        plot_data[0].append(counter)
        
        if latency > 0 :
            success+=1
            plot_data[1].append(latency)
            size+=len(x)
        else:
            plot_data[1].append(0)

        print('Latency: {}'.format(latency))
    
    p = list()
    plt.plot(plot_data[0],p)
    plt.title('Packet\'s latency with 8 intermediate pods')
    plt.xlabel('packets')
    plt.ylabel('latency in S')
    plt.show()
    os.makedirs("plots", exist_ok=True)
    
    i=0
    while True:
        if not os.path.exists("plots/img_{}.png".format(i)):
            break
        i+=1
    plt.savefig("plots/img_{}.png".format(i))


analyze()