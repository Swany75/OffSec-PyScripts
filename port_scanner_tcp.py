#!/usr/bin/env python3

import sys
import socket
import signal
import argparse
from colorama import Fore
from concurrent.futures import ThreadPoolExecutor
from modules.my_utils import show_message
from modules.exit_handler import setup_signal_handler

### Variables & Constants ###########################################################################################################

open_sockets = []

TIMEOUT = 1
MAX_THREADS = 100

### Functions #######################################################################################################################

def close_sockets():
    for socket in open_sockets:
        try:
            socket.close()

        except:
            pass

    open_sockets.clear()

def get_arguments():
    
    parser = argparse.ArgumentParser(description=f'{Fore.GREEN}Fast TCP Port Scanner{Fore.RESET}')
    parser.add_argument("-t", "--target", dest="target", required=True, help="Victim target to scann (Ex: -t 192.168.1.100)")
    parser.add_argument("-p", "--port", dest="ports_str", required=True, help="Port range to scann (Ex: -p 1-100 | Ex: -p 22,23,80,443)")
    options = parser.parse_args()
    
    if options.target is None or options.ports_str is None:
        parser.print_help()
        sys.exit(1)

    return options.target, options.ports_str


def create_socket():
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT)

    open_sockets.append(s)

    return s


def port_scanner(port, host):
    
    s = create_socket()

    try:
        s.connect((host, port))
        print(f"{Fore.YELLOW}[+] {Fore.CYAN}Port: {Fore.WHITE}{port} {Fore.CYAN} is {Fore.GREEN} open")

    except (socket.timeout, ConnectionRefusedError):
        # show_message(f"Port: {Fore.WHITE}{port} {Fore.CYAN} is {Fore.red} closed", "minus")
        pass
     
    finally:
        s.close()

def scan_ports(ports, host):
    
    """
    Escaneja de manera concurrent una llista de ports a un host especificat.

    Aquesta funció utilitza ThreadPoolExecutor per crear un grup de fils (threads)
    que executen simultàniament la funció port_scanner() per a cada port.

    La funció lambda s'utilitza per passar tant el número de port com l'adreça de l'host
    a port_scanner, ja que executor.map() per defecte només admet una llista d'un sol paràmetre.
    """

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(lambda port: port_scanner(port, host), ports)


def parse_ports(ports_str):

    if '-' in ports_str:
        start, end = map(int, ports_str.split('-'))
        return range(start, end + 1)
    
    elif ',' in ports_str:
        return map(int, ports_str.split(','))

    else:
        return (int(ports_str),)


### Main Code #######################################################################################################################

def main():

    show_message(f"Executing:", "info", f"Port Scanner {Fore.YELLOW}TCP")
    setup_signal_handler(close_sockets)

    target, ports_str = get_arguments()
    ports = parse_ports(ports_str)
    scan_ports(ports, target)
   
    show_message("Scan completed successfully!", "info")

if __name__ == "__main__":
    main()
