#!/bin/bash

ip=$1

if [ -z "$1" ]; then
    echo "Usage: $0 <IP address>"
    exit 0
fi


# Reset all counters and iptables rules
iptables -Z && iptables -F
# Measure incoming traffic to the given IP
iptables -I INPUT 1 -s $ip -j ACCEPT
# Measure outgoing traffic to the given IP:
iptables -I OUTPUT 1 -d $ip -j ACCEPT
