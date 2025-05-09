#!/usr/bin/env python3

import sys
import argparse
import scapy.all as scapy
from colorama import Fore
from concurrent.futures import ThreadPoolExecutor
from modules.my_utils import show_message, setup_signal_handler

### Functions #############################################################################################################

def get_arguments():
    parser = argparse.ArgumentParser(description="Tool to discover active hosts in a network using ARP")
    parser.add_argument("-t", "--target", required=True, dest="target", help="Host or network range to scan")
    
    args = parser.parse_args()
    return args.target

def parse_target(target_str):

    # 192.168.1.1-100
    target_str_splitted = target_str.split('.')
    first_three_octets = '.'.join(target_str_splitted[:3])
    
    if len(target_str_splitted) == 4:
        if "-" in target_str_splitted[3]:
            start, end = target_str_splitted[3].split('-')
            return [f"{first_three_octets}.{i}" for i in range(int(start), int(end)+1)]
        else:
            return [target_str]
    else:
        show_error("Invalid IP or IP range format", "error")
        sys.exit(1)

def scan(ip):    
    arp_packet = scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    arp_packet = broadcast_packet/arp_packet
    answered, unanswered = scapy.srp(arp_packet, timeout = 1, verbose = False)
        
    for sent, recived in answered:
        print(f"{Fore.YELLOW}[-] {Fore.CYAN}IP: {Fore.GREEN}{recived.psrc}\t{Fore.CYAN}MAC: {Fore.GREEN}{recived.hwsrc}")

### Main Code #############################################################################################################

def main():
    setup_signal_handler()
    show_message("Executing:", "info", f"Network Scanner {Fore.YELLOW}ARP")

    target_str = get_arguments()
    targets = parse_target(target_str)
   
    show_message("Active hosts on the network:")
    
    max_threads = 100
    
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        executor.map(scan, targets)

    show_message("If you don't see any output:", "info", "Execute this script with root permissions")

if __name__ == "__main__":
    main()
