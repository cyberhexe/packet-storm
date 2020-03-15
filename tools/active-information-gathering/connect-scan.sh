#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <ip> <port-range>"
    exit 0
fi


nc -nvv -w 1 -z $1 $2 2>/dev/null
