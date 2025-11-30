from scapy.all import Ether, IP, TCP, wrpcap, get_if_hwaddr
import sys


current_pod_ip = '10.244.246.129'
dst_ip = '10.244.246.130'
iface = 'eth0'
dst_port = 60000
count = int(sys.argv[1])

pkts = []
for i in range(count):
    sport = 10000 + i
    payload = f"pkt{i}"
    
    pkt = (
        Ether(src=get_if_hwaddr(iface), dst='ee:ee:ee:ee:ee:ee') 
        / IP(src=current_pod_ip, dst=dst_ip) 
        / TCP(sport=sport, dport=dst_port) 
        / payload
    )
    
    pkts.append(pkt)

wrpcap("src.pcap", pkts)

print(f"wrote {len(pkts)} packets to src.pcap")