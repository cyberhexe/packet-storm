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

xvfb-run -s '-terminate' cherrytree -t . "$ctb_file" &&
mv "$ctb_file"_TXT "$output_dir" &&
echo OKAY