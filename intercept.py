import scapy.all as scapy

def process_packet(packet):
    if packet.haslayer(scapy.DNSRR):
        qname = packet[scapy.DNSQR].qname
        print(qname)
        #print(packet.show())
    
scapy.sniff(iface="enp4s0", filter="udp and port 53", prn=process_packet, store=0)
