#!/bin/bash

dirname=$(pwd)


docker run -p 80:80 \
  -v $dirname":/tmp/http" \
  --rm -it python python3 -m http.server 80 \
  --directory '/tmp/http'
