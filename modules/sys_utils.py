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
        # Crear taula i cadena si no existeixen (pot fallar si ja existeixen, però es pot ignorar)
        subprocess.run(['nft', 'add', 'table', 'ip', 'filter'], stderr=subprocess.DEVNULL)
        subprocess.run(['nft', 'add', 'chain', 'ip', 'filter', 'forward', '{ type filter hook forward priority 0 ; policy accept ; }'], stderr=subprocess.DEVNULL)
        # Regla base per forwarding (acceptar)
        subprocess.run(['nft', 'add', 'rule', 'ip', 'filter', 'forward', 'accept'], stderr=subprocess.DEVNULL)

        show_message("IPv4 forwarding activat i regles base configurades correctament.", "plus")

    except subprocess.CalledProcessError as e:
        show_message("Error activant regles base:", "error", f"{e}")
        sys.exit(1)

def setup_nfqueue():
    try:
        subprocess.run("nft add chain ip filter INPUT '{ type filter hook input priority 0; policy accept; }'", shell=True, check=True)
        subprocess.run("nft add chain ip filter OUTPUT '{ type filter hook output priority 0; policy accept; }'", shell=True, check=True)
        subprocess.run("nft add chain ip filter FORWARD '{ type filter hook forward priority 0; policy accept; }'", shell=True, check=True)
        subprocess.run("nft add rule ip filter INPUT queue num 0", shell=True, check=True)
        subprocess.run("nft add rule ip filter OUTPUT queue num 0", shell=True, check=True)
        subprocess.run("nft add rule ip filter FORWARD queue num 0", shell=True, check=True)

        show_message("NFQUEUE rules for DNS Spoofer applied successfully", "plus")

    except subprocess.CalledProcessError as e:
        show_message("Error afegint regles NFQUEUE:", "error", f"{e}")

def disable_rules():
    try:
        subprocess.run("sysctl -w net.ipv4.ip_forward=0", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run("nft flush ruleset", shell=True, check=True)

        show_message("Encaminament desactivat i regles nftables esborrades.", "minus")

    except subprocess.CalledProcessError as e:
        show_message("Error desactivant regles:", "error", f"{e}")
