import matplotlib.pyplot as plt
from scapy.all import *
import statistics

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
                
                latency = dst_pkt.time - src_dict[dst_pkt_bytes]
                latencies.append(latency if latency > 0 else 0)
        
        mean_latency = statistics.mean(latencies)
        median_latency = statistics.median(latencies)

        plot_data[1].append(mean_latency)
        plot_data[2].append(median_latency)
    
    os.makedirs("plots", exist_ok=True)

    plt.plot(plot_data[0], plot_data[1], marker="o", label="mean")
    plt.plot(plot_data[0], plot_data[2], marker="s", label="median")
    plt.title(f"Overall packets latency")
    plt.xlabel("intermediate pods")
    plt.ylabel("latency (seconds)")
    plt.grid(True)
    plt.legend()
    plt.savefig(os.path.join("plots", f"packets_latency.png"), dpi=200)
    plt.show()
    plt.figure()
