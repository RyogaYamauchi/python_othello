from scapy.all import *

user_id = random.randint(0,10000)

# packetの作成。127.0.0.1はローカルホスト（自分のパソコン）
raw = "user_id:" + str(user_id) + ",x:1,y:2"
packet = Ether(src = "1c:36:bb:15:a0:e8 ", dst="1c:36:bb:15:a0:e8 ")/IP(dst="192.168.18.121")/UDP(sport=7, dport=7)/Raw(raw)

# 送信
sendp(packet)

pkts = sniff(iface="en0", filter="udp port 7", count=1)
pkt = pkts[0]
print("client recieved: " + pkt[Raw].load.decode())
