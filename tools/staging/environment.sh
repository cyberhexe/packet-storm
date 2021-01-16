#!/bin/bash

rm -rf /usr/bin/centos-shell &&
rm -rf /usr/bin/impacket &&
rm -rf /usr/bin/tomcat &&
rm -rf /usr/bin/ubuntu-shell &&

link centos-shell.sh /usr/bin/centos-shell &&
link impacket-smb-server.sh /usr/bin/impacket &&
link tomcat.sh /usr/bin/tomcat &&
link ubuntu-shel.sh /usr/bin/ubuntu-shell
