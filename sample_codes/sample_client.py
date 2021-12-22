from scapy.all import *

# packetの作成。127.0.0.1はローカルホスト（自分のパソコン）
packet = Ether(src = "1c:36:bb:15:a0:e8 ", dst="1c:36:bb:15:a0:e8 ")/IP(dst="192.168.18.121")/UDP(sport=7, dport=7)/Raw(b'    ')

# 送信
sendp(packet)

pkts = sniff(iface="en0", filter="udp port 7", count=1)
pkt = pkts[0]
print("client recieved: " + pkt[Raw].load.decode())
