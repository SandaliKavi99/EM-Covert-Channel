from scapy.all import *
from typing import List
import logging, time
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

class PacketSender():
    
    packet: UDP
    iface: str
    frags: List[str]
    count: int
    
    def __init__(self, dest: str="192.168.1.2", count: int = 50, iface: str = "eth0") -> None:
        payload = b'\xff' * 1472
        self.iface = iface
        self.count = count
        self.packet = IP(dst = dest, proto=17)/UDP()/payload
        self.frags = fragment(self.packet)
    
    
    def sendPackets(self) -> None:
        # for f in self.frags:
        #     send(f, verbose = False, iface=self.iface)
        send(self.packet, count = self.count, verbose = False, iface = self.iface)
        # print("...")



if __name__ == "__main__":
    sender = PacketSender()
    
