#!/usr/bin/env bash

# Simple HEX to ASCII converter

# $1 is the first argument given after the bash script
# Check if argument was given, if not - print usage

if [ -z "$1" ]; then
    echo "Usage: $0 <hex string, only digits>"
    exit 0
fi

echo $1 | xxd -r -p
