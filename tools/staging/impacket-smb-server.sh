#!/bin/bash

#alias impacket="docker run --rm -it rflathers/impacket"

if [ -z "$1" ]; then
    echo "Usage: $0 <folder>"
    exit 0
fi


docker run --rm -it -p 445:445 \
  -v $1":/tmp/serve" \
  rflathers/impacket smbserver.py \
  -smb2support my-awesome-share /tmp/serve
