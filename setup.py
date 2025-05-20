#!/usr/bin/env python3

import os
import shutil
from git import Repo
from modules.my_utils import show_message

def install_firefox_decrypt():
    repo_url = 'https://github.com/unode/firefox_decrypt.git'
    ruta_clon = './websites/test_website/firefox_decrypt'
    desti = './websites/test_website/firefox_decrypt.py'

    if not os.path.exists(ruta_clon):
        Repo.clone_from(repo_url, ruta_clon)

    origen = os.path.join(ruta_clon, 'firefox_decrypt.py')
    if os.path.exists(origen):
        shutil.move(origen, desti)
        shutil.rmtree(ruta_clon)
        show_message("Instalat correctament firefox_decrypt")

def main():
    install_firefox_decrypt()

if __name__ == "__main__":
    try:
        show_message("Welcome to:", "info", "Offensive Security Python Scripts")
        main()
    except Exception as e:
        show_message(f"Error: {e}", "error")
