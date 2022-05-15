#!/bin/bash

path="./docs/Cybersecurity/"


inotifywait -r -q -m -e close_write "$path" |
while read -r filename event; do
  rm -rf ./index.html
  find . -name *.md -exec pandoc -f markdown '{}' >> ./index.html \; 
  rm -rf /var/www/html/index.html
  cp ./index.html /var/www/html/
done
