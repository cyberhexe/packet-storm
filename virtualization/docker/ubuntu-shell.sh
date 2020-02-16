#!/bin/bash

dirname=${PWD##*/}
image='ubuntu:18.04'

docker run \
  --rm -it \
  --entrypoint=/bin/bash \
  -v `pwd`:/${dirname} \
  -w /${dirname} \
  $image