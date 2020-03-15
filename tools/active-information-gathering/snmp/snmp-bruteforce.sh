#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <file with ip addresses>"
    exit 0
fi

file_with_ips=$1
password_file=/root/labs/pwk-rabbit-hole/wordlist/snmp/snmp-default.txt

for ip in $(cat $file_with_ips); do
    hydra -P $password_file $ip snmp |tee bruteforce.txt
done
