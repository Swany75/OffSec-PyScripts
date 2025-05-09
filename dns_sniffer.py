#!/usr/bin/env python3

import sys
import argparse
import scapy.all as scapy
from colorama import Fore
from module import setup_signal_handler

### Functions #############################################################################################################

def get_arguments():
    parser = argparse.ArgumentParser(description=f'{Fore.GREEN}DNS Sniffer{Fore.RESET}')
    parser.add_argument("-i", "--interface", dest="interface", required=True, help="Select the interface to sniff (Ex: -i eth0)")

    options = parser.parse_args()
    
    if options.interface is None:
        parser.print_help()
        sys.exit(1)

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
                    print(f"{Fore.YELLOW}[+] {Fore.CYAN}Dominio: {Fore.WHITE}{domain}{Fore.RESET}")

        except Exception as e:
            print(f"{Fore.RED}[!] {Fore.YELLOW}Error processant el paquet DNS: {Fore.WHITE}{e}{Fore.RESET}")

def sniff(interface):
    scapy.sniff(iface=interface, filter="udp and port 53", prn=process_dns_packet, store=0)

### Main Code #############################################################################################################

def main():

    try:
        setup_signal_handler()

        global domains_seen
        domains_seen = set()
        interface = get_arguments()

        print(f"\n{Fore.YELLOW}[+] {Fore.CYAN}Interceptando paquetes de la máquina víctima\n")
        sniff(interface)

    except PermissionError:
         print(f"{Fore.RED}[!] {Fore.YELLOW}You need to be SuperUser to perform this script")
         sys.exit(1)

if __name__ == "__main__":
    main()
