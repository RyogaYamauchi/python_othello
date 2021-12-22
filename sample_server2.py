from scapy.all import *
import time

packet = Ether(src = "1c:36:bb:15:a0:e8 ", dst="1c:36:bb:15:a0:e8 ")/IP(dst="192.168.18.121")/UDP(sport=7, dport=7)/Raw(b'    ')

while(True):
    pkts = sniff(iface="en0", filter="udp port 7", count=1)
    pkt = pkts[0]
    print("server recieved: " + pkt[Raw].load.decode())
    print("wait 1sec...")
    time.sleep(1)
    sendp(packet)
