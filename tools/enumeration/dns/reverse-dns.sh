#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <file with ip addresses>"
    exit 0
fi


#read a file with ip addresses
ip_addresses=$1

#get the subnet
subnet=$(head -n 1 $ip_addresses |cut -d"." -f1,2,3)

#read the first entry of the Class C network (should be sorted by ASC)
start_addr=$(head -n 1 $ip_addresses |cut -d"." -f4)

#same as for the start_addr
end_addr=$(tail -n 1 $ip_addresses |cut -d"." -f4)

for addr in $(seq $start_addr $end_addr);do
    host $subnet.$addr |grep pointer |cut -d" " -f1,5 &
done
