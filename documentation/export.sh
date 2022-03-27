#!/bin/bash

import_cherrytree_notebook="pentest-glossary.ctb"
export_folder_name="glossary-export"

echo "Installing cherrytree and xvfb"
sudo apt install xvfb cherrytree -y || exit 1


echo "Cleaning old export folder"
rm -rf "$export_folder_name"

echo "Exporting the notebook"
xvfb-run cherrytree -t "$export_folder_name" $import_cherrytree_notebook || exit 1
echo "OK"