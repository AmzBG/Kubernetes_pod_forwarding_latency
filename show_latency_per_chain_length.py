import matplotlib.pyplot as plt
from scapy.all import *
import os


def build_dictionary(pkts):
    """
    Builds a dictionary where key: packet's payload (bytes), and value: time
    """
    dictionary = {}
    
    for pkt in pkts:
        dictionary[pkt[Raw].load] = pkt.time
    
    return dictionary


if __name__ == "__main__":


    first_pod = 2
    dirs = list(range(3, 10))
    
    for last_pod in dirs:
        
        intermediate_pods = last_pod - first_pod - 1
        
        src_pkts = rdpcap(f"./packets/{first_pod}-{last_pod}/pod{first_pod}.pcap")
        dst_pkts = rdpcap(f"./packets/{first_pod}-{last_pod}/pod{last_pod}.pcap")

        src_dict = build_dictionary(src_pkts)
        plot_data = [[], []]
        counter = 0
        for dst_pkt in dst_pkts:
            
            dst_pkt_bytes = dst_pkt[Raw].load
            
            if dst_pkt_bytes in src_dict:
                counter += 1
                plot_data[0].append(counter)
                latency = dst_pkt.time - src_dict[dst_pkt_bytes]
                plot_data[1].append(latency if latency > 0 else 0)

        
        os.makedirs("plots/per_chain", exist_ok=True)

        plt.plot(plot_data[0], plot_data[1])
        plt.title(f"Packets latency with {intermediate_pods} intermediate pods")
        plt.xlabel("packets")
        plt.ylabel("latency (seconds)")
        plt.grid(True)
        plt.savefig(os.path.join("plots/per_chain", f"packets_latency_with_{intermediate_pods}_intermediate_pods.png"), dpi=200)
        plt.show()
