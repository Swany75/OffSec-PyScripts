#/usr/bin/env python3

import netifaces
import subprocess
import scapy.all as scapy
from scapy.all import get_if_addr
from colorama import Fore
from .my_utils import show_message
#from my_utils import show_message

### Functions #######################################################################################################################

def get_ip(interface):
    try:
        ip = get_if_addr(interface)
        return ip

    except Exception as e:
        show_message(f"Error obtenint la IP de {Fore.GREEN}{interface}", "error", e)
        return None

def get_gateway(interface):
    try:
        result = subprocess.run(f"ip route show dev {interface} | grep default", shell=True, capture_output=True, text=True)
        lines = result.stdout.strip().splitlines()
        for line in lines:
            parts = line.split()
            if "default" in parts and "via" in parts:
                return parts[parts.index("via") + 1]
    except Exception as e:
        show_message(f"No s'ha pogut obtenir la gateway per la interfície {interface}", "error", e)
    return None

def get_mac(ip):
    answered, _ = scapy.arping(ip, timeout=2, verbose=False)
    
    if answered:
        return answered[0][1].hwsrc
    
    return None

def get_own_mac(interface):
    try:
        return netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
    
    except Exception as e:
        show_message("ERROR:", "error", e)
        return None

