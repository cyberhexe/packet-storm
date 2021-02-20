#!/bin/bash

#alias impacket="docker run --rm -it rflathers/impacket"

if [ -z "$1" ]; then
    echo "Usage: $0 <filepath>"
    exit 0
fi

file_name=$1
output_file='hex-dump.txt'

xxd $file_name |cut -d" " -f 2-9 |sed 's/ //g' |tr -d '\n' > $output_file &&

cat $output_file
