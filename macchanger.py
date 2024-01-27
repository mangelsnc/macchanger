#!/usr/bin/env python3

import argparse
import os
import re
import signal
import socket
import subprocess
import sys
from termcolor import colored

def change_mac(iface, new_address):
    print(colored(f"\n[+] Changing {iface} MAC address to {new_address}...", 'green'))

    if os.geteuid() != 0:
        print(colored(f"\n[!] You need to be root to change the MAC address", 'red'))
        sys.exit(1)

    if not is_valid_mac(new_address):
        print(colored(f"\n[!] Invalid MAC address: {new_address}", 'red'))
        sys.exit(2)
    
    if not is_valid_iface(iface):
        print(colored(f"\n[!] Invalid iface: {iface}", 'red'))
        sys.exit(3)

    subprocess.run(['ifconfig', iface, 'down'])
    subprocess.run(['ifconfig', iface, 'hw', 'ether', new_address])
    subprocess.run(['ifconfig', iface, 'up'])

    print(colored(f"[+] MAC address on {iface} was changed successfully", 'green'))

def is_valid_mac(new_address):
    VALID_MAC_ADDRESS = r'^([A-F0-9]{2}:){5}[A-F0-9]{2}$'
    
    return re.match(VALID_MAC_ADDRESS, new_address)

def is_valid_iface(iface):
    valid_ifaces = [iface[1] for iface in socket.if_nameindex()]

    return iface in valid_ifaces

def get_arguments():
    parser = argparse.ArgumentParser(prog='macchanger', description='MAC address changer')
    parser.add_argument('-i', '--iface', dest='iface', required=True, help='Interface to change the MAC address. Ex: -i eth0 } -iface eth0')
    parser.add_argument('-m', '--mac', dest='new_address', required=True, help='New MAC address. Ex: -m CA:FE:CA:FE:CA:FE | --mac CA:FE:CA:FE:CA:FE')
    options = parser.parse_args()

    return options.iface, options.new_address.upper()

def handle_sigint(signal, frame):
    print(colored(f"\n\n[!] Aborting execution...", 'red'))
    subprocess.run(['ifconfig', iface, 'up'])
    sys.exit(1)

if __name__ == "__main__":

    iface, new_address = get_arguments()

    signal.signal(signal.SIGINT, handle_sigint)
    
    change_mac(iface, new_address)
