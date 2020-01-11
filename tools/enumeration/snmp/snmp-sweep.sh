#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <ip>"
    exit 0
fi

ip=$1

nmap -p161 -sU --open $ip -oG snmp-sweep.nmap &&
grep Up snmp-sweep.nmap |cut -d" " -f2 > snmp-ips.txt &&
rm -rf snmp-sweep.nmap
echo 'OK.'
