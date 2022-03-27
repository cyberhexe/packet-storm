#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <target cherrytree file> "
    exit 0
fi

import_cherrytree_notebook="$1"
export_folder_name="cherrytree-export"

echo "Cleaning old export folder"
rm -rf "$export_folder_name"

echo "Exporting the notebook"
cherrytree -t "$export_folder_name" "$import_cherrytree_notebook" || exit 1
echo "OK"