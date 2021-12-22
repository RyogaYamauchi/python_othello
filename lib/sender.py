from scapy.all import *
import lib.deserializer as deserializer
import lib.packet_builder as packet_builder

class Sender():
    def send(instance):
        desirialized= deserializer.Deserializer.deserialize(instance)
        packet = packet_builder.PacketBuilder.build(desirialized)
        print("#sender log : " + desirialized)
        sendp(packet) # リクエストを送信
