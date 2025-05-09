#!/usr/bin/env python3

import sys
import signal
from .my_utils import show_message

_exit_callback = None

def setup_signal_handler(callback=None):
    global _exit_callback
    _exit_callback = callback
    signal.signal(signal.SIGINT, _handler)  # Ctrl+C

def _handler(sig, frame):
    exit_program()

def exit_program():
    if _exit_callback:
        _exit_callback()  # Es crida només si s’ha passat
    show_message("Exiting the program...", "error")
    sys.exit(1)
