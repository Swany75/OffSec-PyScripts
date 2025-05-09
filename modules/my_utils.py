#!/usr/bin/env python3

import sys
import signal
from colorama import Fore

### Functions #######################################################################################################################

def show_message(message, symbol="plus", extra=""):
    if symbol == "error":
        print(f"\n\n{Fore.RED}[!] {Fore.YELLOW}{message} {Fore.WHITE}{extra}{Fore.RESET}\n")
    
    elif symbol == "info":
        print(f"\n{Fore.GREEN}[i] {Fore.CYAN}{message} {Fore.RED}{extra}{Fore.RESET}\n")
    
    elif symbol == "minus":
        print(f"\n{Fore.YELLOW}[-] {Fore.CYAN}{message} {Fore.WHITE}{extra}{Fore.RESET}\n")
    
    elif symbol == "plus":
        print(f"\n{Fore.YELLOW}[+] {Fore.CYAN}{message} {Fore.WHITE}{extra}{Fore.RESET}\n")
