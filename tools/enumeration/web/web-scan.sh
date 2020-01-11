#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <file with IP addresses>"
    exit 0
fi

file_with_addresses=$1

nmap -sV -sC -p80 -O -iL $file_with_addresses -oN web-scan.nmap &&
echo 'OK.'
