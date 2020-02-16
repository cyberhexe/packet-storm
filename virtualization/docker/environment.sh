#!/bin/bash

rm -rf /usr/bin/docker-centos-shell &&
rm -rf /usr/bin/docker-python-http-server &&
rm -rf /usr/bin/docker-smb-share &&
rm -rf /usr/bin/docker-tomcat &&
rm -rf /usr/bin/docker-ubuntu-shell &&

link centos-shell.sh /usr/bin/docker-centos-shell &&
link python-http-server.sh /usr/bin/docker-python-http-server &&
link smb-share.sh /usr/bin/docker-smb-share &&
link tomcat.sh /usr/bin/docker-tomcat &&
link ubuntu-shell.sh /usr/bin/docker-ubuntu-shell
