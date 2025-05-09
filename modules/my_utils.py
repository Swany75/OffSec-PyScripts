#!/usr/bin/env python3

import os
import sys
import signal
import smtplib
import netifaces
import subprocess
import scapy.all as scapy
from colorama import Fore, Style
from email.mime.text import MIMEText

def exit_program():
    show_message("Exiting the program...", "error")
    sys.exit(1)

def _handler(sig, frame):
    exit_program()

def setup_signal_handler():
    signal.signal(signal.SIGINT, _handler)

### Network Utils ###################################################################################################################

def exit(parser):
    parser.print_help()
    sys.exit(1)

### Show better messages ############################################################################################################

"""

My idea with this messages are:
- Plus:  [+] Hey there im the script
- Minus: [-] You recive this output
- Info:  [i] Script X is executing
- Error: [!] Error: You are dumb

"""

def show_message(message, symbol="plus", extra=""):
    if symbol == "error":
        print(f"\n\n{Fore.RED}[!] {Fore.YELLOW}{message} {Fore.WHITE}{extra}{Fore.RESET}\n")
    
    elif symbol == "info":
        print(f"\n{Fore.GREEN}[i] {Fore.CYAN}{message} {Fore.RED}{extra}{Fore.RESET}\n")
    
    elif symbol == "minus":
        print(f"\n{Fore.YELLOW}[-] {Fore.CYAN}{message} {Fore.WHITE}{extra}{Fore.RESET}\n")
    
    elif symbol == "plus":
        print(f"\n{Fore.YELLOW}[+] {Fore.CYAN}{message} {Fore.WHITE}{extra}{Fore.RESET}\n")

### Credentials #####################################################################################################################

def get_credentials(file):
    try:
        with open(f'credentials/{file}.txt', encoding="utf-8") as f:
            lines = f.readlines()

    except FileNotFoundError as e:
        show_message(f"No s'ha trobat el fitxer 'credentials/{file}'.txt: ", "error", e)
        return None

    if len(lines) < 2 or not lines[1].strip():
        show_message(f"No s'ha trobat cap dada a la segona línia de '{file}'. Escriu-la sota el comentari.", "error")
        return None

    return lines[1].strip()

### Mail Functions ##################################################################################################################

def smail(subject, body, sender, recipients, password):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())

        show_message("Email sent successfully")

    except Exception as e:
        show_message(f"Error sending email: {str(e)}", "error")
