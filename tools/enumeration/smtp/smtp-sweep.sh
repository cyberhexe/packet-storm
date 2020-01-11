#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <ip>"
    exit 0
fi

ip=$1

nmap -p25 --open $ip -oG smtp-sweep.nmap &&
clear &&
grep Up smtp-sweep.nmap |cut -d" " -f2

