#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <target domain> <domains wordlist>"
    exit 0
fi

if [ -z "$2" ]; then
    echo "Usage: $0 <target domain> <domain wordlist>"
    exit 0
fi


domains_file=$2
domain=$1

for subdomain in $(cat $domains_file);do
    host $subdomain.$domain |grep "has address" |cut -d" " -f1,4 &
done
