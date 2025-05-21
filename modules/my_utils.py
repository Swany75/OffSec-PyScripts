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

def print_demon():

    print(f"""{Fore.RED}

          .                                                      .
        .n                   .                 .                  n.
  .   .dP                  dP                   9b                 9b.    .
 4    qXb         .       dX                     Xb       .        dXp     t
dX.    9Xb      .dXb    __                         __    dXb.     dXP     .Xb
9XXb._       _.dXXXXb dXXXXbo.                 .odXXXXb dXXXXb._       _.dXXP
 9XXXXXXXXXXXXXXXXXXXVXXXXXXXXOo.           .oOXXXXXXXXVXXXXXXXXXXXXXXXXXXXP
  `9XXXXXXXXXXXXXXXXXXXXX'~   ~`OOO8b   d8OOO'~   ~`XXXXXXXXXXXXXXXXXXXXXP'
    `9XXXXXXXXXXXP' `9XX'          `98v8P'          `XXP' `9XXXXXXXXXXXP'
        ~~~~~~~       9X.          .db|db.          .XP       ~~~~~~~
                        )b.  .dbo.dP'`v'`9b.odb.  .dX(
                      ,dXXXXXXXXXXXb     dXXXXXXXXXXXb.
                     dXXXXXXXXXXXP'   .   `9XXXXXXXXXXXb
                    dXXXXXXXXXXXXb   d|b   dXXXXXXXXXXXXb
                    9XXb'   `XXXXXb.dX|Xb.dXXXXX'   `dXXP
                     `'      9XXXXXX(   )XXXXXXP      `'
                              XXXX X.`v'.X XXXX
                              XP^X'`b   d'`X^XX
                              X. 9  `   '  P )X
                              `b  `       '  d'
                               `             '

{Fore.RESET}""")
