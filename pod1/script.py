import random
import socket
from time import sleep
import sys
from scapy.all import *
from scapy.layers.l2 import *
from scapy.layers.inet import *

iface = 'eth0'
dport = 60000
i = 1

# pod2 ip (ingress)
current_pod_ip = '10.244.246.129'
dst = '10.244.246.130'

if __name__ == "__main__":
    # test if is a valid interface
    if (iface not in get_if_list()):
        print(' [{0}] inteface not found .'.format(iface))
        print('list of interfaces :', get_if_list())
    else:
        while (True):
            sport = random.randint(49152, 65535)
            to = socket.gethostbyname(dst)
            print("------to: ", to, "--------")
            if (i % 2 == 0):
                msg = 'Hello word ({0}) uplink'.format(i)
            else:
                msg = 'Hello word ({0}) downlink'.format(i)

            pkt = Ether(src=get_if_hwaddr(iface), dst='ee:ee:ee:ee:ee:ee') / IP(src=current_pod_ip, dst=to) / TCP(dport=dport, sport=sport) / msg

            pkt.show2()
            sys.stdout.flush()

            print('------ pod 1 sending ------')
            sendp(pkt, iface=iface, verbose=True)

            i += 1
            sleep(4)
