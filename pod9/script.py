import sys
from scapy.all import *
from scapy.layers.l2 import *
from scapy.layers.inet import *


iface = 'eth0'
dport = 60000

#pods ip
current_pod_ip = '10.244.246.137'

def handle_pkt(pkt, packets_received):
    if TCP in pkt and pkt[TCP].dport == 60000 and str(pkt[IP].dst) == current_pod_ip :
        
        packets_received += 1

        data = pkt[Raw].load
        
        pkt.show()
        sys.stdout.flush()
        print('\n')
        print('\n')
        
        print(f"Got packet with this: {data}")
        print(f"So far {packets_received} packets recieved over all!")
        
        print('\n')
        print('\n')


if __name__ == "__main__":
    packets_received = 0
    sniff(filter="tcp and port 60000" ,iface = iface, prn = lambda x: handle_pkt(x, packets_received))