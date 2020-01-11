#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <ip>"
    exit 0
fi

ip=$1

nmap -n -sn $ip -oG ping-sweep.nmap &&
grep Up ping-sweep.nmap |cut -d" " -f2 > up_addresses.txt

cat up_addresses.txt
