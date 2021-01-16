#!/bin/bash

dirname=${PWD##*/}
image='tomcat:8'

docker run \
  --rm -it \
  --entrypoint=/bin/bash \
  -v `pwd`:/${dirname} \
  $image
