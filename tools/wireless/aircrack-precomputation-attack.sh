#!/bin/bash

# Use this script to compute hash tables and run aircrack-ng for cracking the WPA handshake

if [ -z "$1" ]; then
    echo "Usage: $0 <passwd-file> <essid-file> <cap-file>"
    exit 0
fi

if [ -z "$2" ]; then
    echo "Usage: $0 <passwd-file> <essid-file> <cap-file>"
    exit 0
fi

if [ -z "$3" ]; then
    echo "Usage: $0 <passwd-file> <essid-file> <cap-file>"
    exit 0
fi

airolib_hash_table='airolib-database'

passwd_file=$1
essid_file=$2
wpa_handshake_file=$3

echo $passwd_file
echo $essid_file
echo $wpa_handshake_file

airolib-ng $airolib_hash_table --import passwd $passwd_file
airolib-ng $airolib_hash_table --import essid $essid_file
airolib-ng $airolib_hash_table --stats
airolib-ng $airolib_hash_table --clean all

airolib-ng $airolib_hash_table --batch
airolib-ng $airolib_hash_table --verify all
aircrack-ng -r $airolib_hash_table out $wpa_handshake_file
