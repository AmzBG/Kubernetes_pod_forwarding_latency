import time
import sys
from scapy.all import get_if_hwaddr, sniff, sendp, Ether, IP, TCP, Raw


# pod ip
current_pod_ip = '10.244.246.137'

iface = 'eth0'

dport = 60000

# packets_received = 0

processing_delay = 0.0

def handle_pkt(pkt):
    pass
    # global packets_received

    # packets_received += 1

    # data = pkt[Raw].load
    
    # pkt.show()
    # print()
    # print(f"Got packet with this: {data}")
    # print(f"So far {packets_received} packets recieved over all!")
    # print()
    # sys.stdout.flush()


if __name__ == "__main__":
    sniff(
        iface=iface,
        filter=f"tcp and dst host {current_pod_ip} and dst port {dport}",
        prn=handle_pkt
    )