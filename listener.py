#!/usr/bin/env python3

import socket
import argparse
from modules.my_utils import show_message
from modules.sys_utils import check_root
from modules.exit_handler import setup_signal_handler
from modules.net_utils import get_ip

### Classes ##################################################################################################################

class Listener:

    def __init__(self, ip, port):

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ip, port))
        server_socket.listen()

        show_message("Listening form incomming connections...")

        self.client_socket, client_address = server_socket.accept()

        show_message("Connection established by", "minus", client_address)

    def execute(self, command):
        self.client_socket.send(command.encode())

        response = b""
        while True:
            chunk = self.client_socket.recv(1024)
            if not chunk or chunk.endswith(b"\n\n"):
                response += chunk
                break
            response += chunk

        return response.decode(errors="ignore")

    def run(self):        
        while True:
            try:
                command = input(">> ").strip()

                if command.lower() == "exit":
                    show_message("Closing connection", "info")
                    self.client_socket.close()
                    break

                output = self.execute(command)
                print(output)

            except BrokenPipeError:
                show_message("Connection lost: Broken pipe", "error")
                break

            except Exception as e:
                show_message("Unexpected error", "error", str(e))
                break

### Functions ################################################################################################################

def get_arguments():
    parser = argparse.ArgumentParser(description="TCP Listener")
    parser.add_argument("-i", "--interface", required=True,
                        help="Network interface to bind listener to (e.g. eth0, wlan0)")

    args = parser.parse_args()
    return args.interface

### Main Code ################################################################################################################

def main():
    check_root()
    setup_signal_handler()

    interface = get_arguments()
    ip = get_ip(interface)

    show_message("Executing:", "info", "TCP Listener")

    my_listener = Listener(ip, 443)
    my_listener.run()

if __name__ == "__main__":
    main()
