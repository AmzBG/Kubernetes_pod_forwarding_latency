import time
import sys
from scapy.all import get_if_hwaddr, sniff, sendp, Ether, IP, TCP, Raw


# pod ips
current_pod_ip = '10.244.246.131'
qos_ip = '10.244.246.132'

dport = 60000
sport = 60001

iface = 'eth0'
src_mac = get_if_hwaddr(iface)

# packets_received = 0

processing_delay = 0.0

def handle_packet(pkt):

    if processing_delay > 0.0:
        time.sleep(processing_delay)
    
    # global packets_received
    
    # packets_received += 1
    
    data = pkt[Raw].load
    
    pkt2 = (
        Ether(src=src_mac, dst='ee:ee:ee:ee:ee:ee') 
        / IP(src=current_pod_ip, dst=qos_ip) 
        / TCP(dport=dport, sport=sport) 
        / data
    )
    
    # pkt.show()
    # print()
    # print(f"Got packet with this: {data}")
    # print(f"So far {packets_received} packets recieved over all!")
    # print()
    # sys.stdout.flush()
    
    sendp(pkt2, iface=iface, verbose=True)

if __name__ == "__main__":
    sniff(
        iface=iface,
        filter=f"tcp and dst host {current_pod_ip} and dst port {dport}",
        prn=handle_packet,
        store=0,
    )