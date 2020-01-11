#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 -p<ports to scan> <ip-address>"
    exit 0
fi

if [ -z "$2" ]; then
    echo "Usage: $0 -p<ports to scan> <ip-address>"
    exit 0
fi


network_scan=nmap-sweep.txt
ports_to_scan=$1
ip=$2
nmap $ports_to_scan $ip --open -oG $network_scan &&
for ip in $(cat $network_scan |grep Up |cut -d" " -f2);do
    # Scanning each target for the vulnerabilities
    mkdir $ip 2>/dev/null
    nmap $ports_to_scan --script vuln --script-args=unsafe=1 $ip -oN ./$ip/vulns.txt
done
rm -rf $network_scan &&
echo 'OK'
