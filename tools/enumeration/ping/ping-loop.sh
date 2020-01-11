#!/bin/bash

network=10.11.1.

for i in $(seq 1 254)
do
   ping -c 1 $network$i |grep "bytes from" |cut -d ":" -f1 |cut -d " " -f4 &
done

