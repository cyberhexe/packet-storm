#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <dns-server> <file-with-ip-addresses>"
    exit 0
fi

dns_server=$1
ips=$2

for ip in $(cat $ips); do
    nslookup $ip $dns_server |grep name &
done
