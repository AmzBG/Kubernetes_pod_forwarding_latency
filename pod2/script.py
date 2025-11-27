import random
import socket
import sys
from scapy.all import *
from scapy.layers.l2 import *
from scapy.layers.inet import *


iface = 'eth0'
dport = 60000


#pods ip
current_pod_ip = '10.244.246.130'
uplink_ip = '10.244.246.131'
# downlink_ip = '10.244.246.132'


def get_pkt():
    while (True):
        pkts = sniff(count=1,filter="tcp and port {0}".format(dport) )
        if TCP in pkts[0] and pkts[0][TCP].dport == dport and str(pkts[0][IP].dst) == current_pod_ip :
            return pkts[0]

if __name__ == "__main__":
    packets_received = 0
    while(True):
        
        pkt = get_pkt()
        packets_received += 1
        
        data = pkt[Raw].load
        
        # msg = str(pkt[Raw].load).lower()
        
        dst = uplink_ip

        # if('down' in msg):
        #     dst = downlink_ip
            
        sport = random.randint(49152,65535)
        to = socket.gethostbyname(dst)
        
        pkt_with_header = Ether(src=get_if_hwaddr(iface), dst='ee:ee:ee:ee:ee:ee') / IP(src=current_pod_ip, dst=to) / TCP(dport=dport , sport=sport ) / data
        
        pkt_with_header.show()
        sys.stdout.flush()
        print('\n')
        print('\n')
        
        print(f"Got packet with this: {data}")
        print(f"So far {packets_received} packets recieved over all!")
        
        print('\n')
        print('\n')
        
        sendp(pkt_with_header,iface=iface,verbose=True)