#!/usr/bin/env python3

import os
import sys
import subprocess
from .my_utils import show_message

### Functions #######################################################################################################################

def check_root():
    if os.geteuid() != 0:
        show_message("Error: You need to run this script as sudo", "error")
        sys.exit(1)

def enable_rules():
    try:
        # Activa l'encaminament IPv4
        subprocess.run("sysctl -w net.ipv4.ip_forward=1", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Crear taula i cadenes
        subprocess.run(r"nft add table ip filter", shell=True, check=True)
        subprocess.run(r"nft add chain ip filter input { type filter hook input priority 0 \; }", shell=True, check=True)
        subprocess.run(r"nft add chain ip filter output { type filter hook output priority 0 \; }", shell=True, check=True)
        subprocess.run(r"nft add chain ip filter forward { type filter hook forward priority 0 \; }", shell=True, check=True)

        # Afegir regles
        subprocess.run(r"nft add rule ip filter input counter queue num 0", shell=True, check=True)
        subprocess.run(r"nft add rule ip filter output counter queue num 0", shell=True, check=True)
        subprocess.run(r"nft add rule ip filter forward counter queue num 0", shell=True, check=True)
        subprocess.run(r"nft add rule ip filter forward accept", shell=True, check=True)

        show_message("IPv4 forwarding activat i regles nftables configurades correctament.", "plus")

    except subprocess.CalledProcessError as e:
        show_message("Error activant regles:", "error", f"{e}")
        sys.exit(1)

def disable_rules():
    try:
        subprocess.run("sysctl -w net.ipv4.ip_forward=0", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run("nft flush ruleset", shell=True, check=True)
        
        show_message("Encaminament desactivat i regles nftables esborrades.", "minus")

    except subprocess.CalledProcessError as e:
        show_message("Error desactivant regles:", "error", f"{e}")
