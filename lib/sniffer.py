from scapy.all import *

class Sniffer():
    def sniff():
        pkts = sniff(iface="en0", filter="udp port 7", count=1)
        # 通信エラー処理もしたい
        return pkts[0][Raw].load.decode('utf-8')
