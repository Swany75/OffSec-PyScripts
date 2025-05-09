#!/usr/bin/env python3

import sys
import argparse
import subprocess
from colorama import Fore
from concurrent.futures import ThreadPoolExecutor
from modules.my_utils import show_message
from modules.exit_handler import setup_signal_handler

### Functions #############################################################################################################

def get_arguments():
    parser = argparse.ArgumentParser(description="Tool to discover active hosts in a network using ICMP")
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

def host_discovery(target):

    try:            
        ping = subprocess.run(["ping", "-c", "1", target], timeout=1, stdout=subprocess.DEVNULL)

        if ping.returncode == 0:
            print(f"{Fore.YELLOW}[-] {Fore.CYAN}IP: {Fore.GREEN}{target} {Fore.CYAN}is active")
    
    except subprocess.TimeoutExpired:
        pass

### Main Code #############################################################################################################

def main():

    setup_signal_handler()
    show_message("Executing", "info", f"Network Scanner {Fore.YELLOW}ICMP")

    target_str = get_arguments()
    targets = parse_target(target_str)

    show_message("Active hosts on the network:")

    max_threads = 100
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        executor.map(host_discovery, targets)

if __name__ == "__main__":
    main()
