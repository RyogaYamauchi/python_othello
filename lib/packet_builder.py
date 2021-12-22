from scapy.all import *

class PacketBuilder():
    def build(data):
        ether_src = "1c:36:bb:15:a0:e8"
        ether_dst = "1c:36:bb:15:a0:e8"
        ip_dst  = "192.168.18.121"
        sport = 7
        dport = 7
        return Ether(src = ether_src, dst= ether_dst)/IP(dst = ip_dst)/UDP(sport=sport, dport=dport)/Raw(str(data))
