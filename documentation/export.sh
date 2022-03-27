#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <target cherrytree file>"
    exit 0
fi

import_cherrytree_notebook="$1"
export_folder_name="cherrytree-export"

echo "Installing cherrytree and xvfb"
sudo add-apt-repository ppa:giuspen/ppa || exit 1
sudo apt update || exit 1
sudo apt install xvfb cherrytree -y || exit 1


echo "Cleaning old export folder"
rm -rf "$export_folder_name"

echo "Exporting the notebook"
xvfb-run cherrytree -t "$export_folder_name" $import_cherrytree_notebook || exit 1
echo "OK"