#!/usr/bin/env python3

import re
import sys
import argparse
import subprocess
from colorama import Fore
from modules.my_utils import show_message
from modules.exit_handler import setup_signal_handler
from modules.sys_utils import check_root

### Functions ##############################################################################################################

def get_arguments():
    parser = argparse.ArgumentParser(description="Herramienta para cambiar la dirección MAC de una interfazd e red")
    parser.add_argument("-i", "--interface", required=True, dest="interface", help="Nombre de la interfaz de red")
    parser.add_argument("-m", "--mac", required=True, dest="mac_address", help="Nueva dirección mac para la interfaz de red")
    
    return parser.parse_args()

def check_input(mac_address):
    
    return re.match(r'^([A-Fa-f0-9]{2}:){5}[A-Fa-f0-9]{2}$', mac_address)

def change_mac_address(interface, mac_address):

    if not check_input(mac_address):
        show_message("The MAC address format is incorrect", "error")
        return

    try:
        subprocess.run(["ifconfig", interface, "down"], check=True, stderr=subprocess.PIPE)
        subprocess.run(["ifconfig", interface, "hw", "ether", mac_address], check=True, stderr=subprocess.PIPE)
        subprocess.run(["ifconfig", interface, "up"], check=True, stderr=subprocess.PIPE)
        
        show_message("The MAC address has been changed successfully\n")

    except subprocess.CalledProcessError as e:
        error_output = e.stderr.decode().strip()
        show_message("Failed to change MAC address:", "error", error_output)
        sys.exit(1)

### Main Code ##############################################################################################################

def main():
    check_root()
    setup_signal_handler()
    args = get_arguments()
    show_message("Executing:", "info", "MAC Changer")
    change_mac_address(args.interface, args.mac_address)

if __name__ == "__main__":
    main()
