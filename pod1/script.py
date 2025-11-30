import time
import sys
from scapy.all import get_if_hwaddr, sniff, sendp, Ether, IP, TCP, Raw


iface = 'eth0'
dport = 60000

# pod ips
current_pod_ip = '10.244.246.129'
dst = '10.244.246.130'

if __name__ == "__main__":
    pass
