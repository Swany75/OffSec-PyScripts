#!/bin/bash

# Colors ANSI
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
WHITE="\033[1;37m"
CYAN="\033[0;36m"
RESET="\033[0m"

# Funció d'error
error_exit() {
    echo -e "${RED}[!]${YELLOW} Error: ${WHITE}$1${RESET}"
    exit 1
}

echo

# Comprovació de permisos
if [ "$EUID" -ne 0 ]; then
    error_exit "Aquest script s'ha d'executar com a root (sudo)"
fi

# Crear taula
nft add table ip filter

# Crear cadenes
nft add chain ip filter input { type filter hook input priority 0 \; }
nft add chain ip filter output { type filter hook output priority 0 \; }
nft add chain ip filter forward { type filter hook forward priority 0 \; }

# Regles de queue
nft add rule ip filter input counter queue num 0
nft add rule ip filter output counter queue num 0
nft add rule ip filter forward counter queue num 0
# Política ACCEPT
nft add rule ip filter forward accept

echo -e "${YELLOW}[+]${CYAN} Configuració de nftables completada correctament.${RESET}"
echo -e "${YELLOW}[+]${CYAN} Per borrar la configuració executa 'nft flush ruleset'${RESET}"
echo
