#!/bin/bash

file_name=$1

for suid in $(cat $file_name); do
    echo Looking exploits for $suid
    searchsploit $suid local linux |grep -v -i "No Result"
    echo '**********************************************'
done
