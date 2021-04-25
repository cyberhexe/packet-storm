#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <.java file>"
    exit 0
fi

class_name=$(echo $1|cut -d"." -f1)

javac -source 1.8 -target 1.8 $1 &&
mkdir META-INF &&
echo "Main-Class: "$class_name > META-INF/MANIFEST.MF &&
jar cmvf META-INF/MANIFEST.MF $class_name.jar $class_name.class &&

rm -rf META-INF &&
rm -rf $class_name.class
