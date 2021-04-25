#!/bin/bash

# use this script to create a fake Access Point (AP)

if [ -z "$1" ]; then
    echo "Usage: $0 <iface-monitor>"
    exit 0
fi

output='captured'

echo 'Writing captured packets to '$output
airbase-ng $1 -F $output -P
