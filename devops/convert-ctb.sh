#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <ctb file> <output directory>"
    exit 0
fi

if [ -z "$2" ]; then
    echo "Usage: $0 <ctb file> <output directory>"
    exit 0
fi

ctb_file="$1"
output_dir="$2"

echo "Converting $ctb_file"

xvfb-run -s '-terminate' cherrytree -x "/tmp" "$1" || exit
mv /tmp/*_HTML/* "$output_dir" || exit
rm -rf /tmp/*_HTML || exit