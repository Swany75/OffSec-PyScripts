#!/usr/bin/env python3

import argparse
import scapy.all as scapy
from colorama import Fore
from modules.my_utils import show_message
from modules.exit_handler import setup_signal_handler
from modules.sys_utils import check_root

### Functions ########################################################################################################################

def get_arguments():
    parser = argparse.ArgumentParser(description='DNS Sniffer')
    parser.add_argument("-i", "--interface", dest="interface", required=True, help="Select the interface to sniff (Ex: -i eth0)")

    options = parser.parse_args()
    return options.interface

def process_dns_packet(packet):
    # print(f"{Fore.YELLOW}[+] {Fore.CYAN}Paquete recibido: {Fore.WHITE}{packet.summary()}{Fore.RESET}")
    if packet.haslayer(scapy.DNSQR):
        try:
            domain = packet[scapy.DNSQR].qname.decode()
                
            if domain:
                exclude_keywords = ["google", "cloud", "bind", "static"]

                if domain not in domains_seen and not any(keyword in domain for keyword in exclude_keywords):
                    domains_seen.add(domain)
                    print(f"{Fore.YELLOW}[-] {Fore.CYAN}Domain: {Fore.WHITE}{domain}")


        except Exception as e:
            show_message("Error while processing DNS packet:", "error", e)

def sniff(interface):
    scapy.sniff(iface=interface, filter="udp and port 53", prn=process_dns_packet, store=0)

### Main Code #############################################################################################################

def main():
    check_root()
    setup_signal_handler()
    show_message("Executing:", "info", "DNS Sniffer")

    global domains_seen
    domains_seen = set()
    interface = get_arguments()

    show_message("Interceptando paquetes de la máquina víctima")
    sniff(interface)

if __name__ == "__main__":
    main()
