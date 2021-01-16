#!/bin/bash

dirname=${PWD##*/}
image='centos'

docker run \
  --rm -it \
  --entrypoint=/bin/bash \
  -v `pwd`:/${dirname} \
  -w /${dirname} \
  $image