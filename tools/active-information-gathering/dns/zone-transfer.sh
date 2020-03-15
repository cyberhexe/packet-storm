#!/bin/bash
#Zone Transfer bash script

if [ -z "$1" ]; then
    echo "Usage: $0 <domain name>"
    exit 0
fi

# If the argument was given, identify the DNS servers for the domain.
# For each of these services, attempt a zone transfer

for server in $(host -t ns $1 |cut -d" " -f4); do
    host -l $1 $server |grep "has address"
done
