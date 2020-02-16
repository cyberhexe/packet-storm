#!/bin/bash

docker run --rm -it -p 445:445 \
  -v "${PWD}:/tmp/serve" \
    rflathers/impacket smbserver.py \
      -smb2support \
      'SHARE' '/tmp/serve'
