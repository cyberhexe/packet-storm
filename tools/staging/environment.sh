#!/bin/bash

rm -rf /usr/bin/centos-shell &&
rm -rf /usr/bin/impacket &&
rm -rf /usr/bin/tomcat &&
rm -rf /usr/bin/ubuntu-shell &&
rm -rf /usr/bin/aws-deploy &&

apt install awscli -y &&
pip3 install boto3 &&

link centos-shell.sh /usr/bin/centos-shell &&
link impacket-smb-server.sh /usr/bin/impacket &&
link tomcat.sh /usr/bin/tomcat &&
link ubuntu-shell.sh /usr/bin/ubuntu-shell
link aws-deploy.py /usr/bin/aws-deploy
