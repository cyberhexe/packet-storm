#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <path-to-jars>"
    exit 0
fi


java -jar jd-cli.jar $1 --outputDir output
