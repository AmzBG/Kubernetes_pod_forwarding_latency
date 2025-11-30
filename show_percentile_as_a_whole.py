import matplotlib.pyplot as plt
from scapy.all import *
import numpy as np
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
    
    plot_data = [[], [], []]

    for last_pod in dirs:
        
        dir_name = f"{first_pod}-{last_pod}"
        src_pkts = rdpcap(f"./packets/{dir_name}/pod{first_pod}.pcap")
        dst_pkts = rdpcap(f"./packets/{dir_name}/pod{last_pod}.pcap")

        intermediate_pods = last_pod - first_pod - 1
    
        plot_data[0].append(intermediate_pods)

        src_dict = build_dictionary(src_pkts)

        latencies = []
        for dst_pkt in dst_pkts:

            dst_pkt_bytes = dst_pkt[Raw].load

            if dst_pkt_bytes in src_dict:
                latency = max(dst_pkt.time - src_dict[dst_pkt_bytes], 0)
                latencies.append(float(latency))
        
        p95 = np.percentile(latencies, 95)
        p99 = np.percentile(latencies, 99)

        plot_data[1].append(p95)
        plot_data[2].append(p99)
    
    os.makedirs("plots", exist_ok=True)

    plt.plot(plot_data[0], plot_data[1], marker="o", label="p95")
    plt.plot(plot_data[0], plot_data[2], marker="s", label="p99")
    plt.title(f"Overall packets percentile")
    plt.xlabel("intermediate pods")
    plt.ylabel("latency (seconds)")
    plt.grid(True)
    plt.legend()
    plt.savefig(os.path.join("plots", f"packets_percentile.png"), dpi=200)
    plt.show()
