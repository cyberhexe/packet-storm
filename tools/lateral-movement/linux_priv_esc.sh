#!/bin/bash

echo "====================================================="
echo "What's the distribution type? What version?"
cat /etc/issue 2>/dev/null
cat /etc/*-release 2>/dev/null
cat /etc/lsb-release 2>/dev/null      # Debian based
cat /etc/redhat-release 2>/dev/null   # Redhat based

echo "====================================================="
echo "What's the kernel version? Is it 64-bit?"
cat /proc/version 2>/dev/null
uname -a 2>/dev/null
uname -mrs 2>/dev/null
rpm -q kernel 2>/dev/null
dmesg | grep Linux 2>/dev/null
ls /boot | grep vmlinuz- 2>/dev/null

echo "====================================================="
echo "What can be learnt from the environmental variables?"
cat /etc/profile 2>/dev/null
cat /etc/bashrc 2>/dev/null
cat ~/.bash_profile 2>/dev/null
cat ~/.bashrc 2>/dev/null
cat ~/.bash_logout 2>/dev/null
env 2>/dev/null
set 2>/dev/null

echo "====================================================="
echo "What services are running? Which service has which user privilege?"
ps aux 2>/dev/null
ps -ef 2>/dev/null
top 2>/dev/null
cat /etc/services 2>/dev/null

echo "====================================================="
echo "Which service(s) are been running by root? Of these services, which are vulnerable - it's worth a double check!"
ps aux | grep root
ps -ef | grep root

echo "====================================================="
echo "What applications are installed? What version are they? Are they currently running?"
ls -alh /usr/bin/ 2>/dev/null
ls -alh /sbin/ 2>/dev/null
dpkg -l 2>/dev/null
rpm -qa 2>/dev/null
ls -alh /var/cache/apt/archivesO 2>/dev/null
ls -alh /var/cache/yum/ 2>/dev/null

echo "====================================================="
echo "Any of the service(s) settings misconfigured? Are any (vulnerable) plugins attached?"
cat /etc/syslog.conf 2>/dev/null
cat /etc/chttp.conf 2>/dev/null
cat /etc/lighttpd.conf 2>/dev/null
cat /etc/cups/cupsd.conf 2>/dev/null
cat /etc/inetd.conf 2>/dev/null
cat /etc/apache2/apache2.conf 2>/dev/null
cat /etc/my.conf 2>/dev/null
cat /etc/httpd/conf/httpd.conf 2>/dev/null
cat /opt/lampp/etc/httpd.conf 2>/dev/null
ls -aRl /etc/ | awk '$1 ~ /^.*r.*/'

echo "====================================================="
echo "What jobs are scheduled?"
crontab -l 2>/dev/null
ls -alh /var/spool/cron 2>/dev/null
ls -al /etc/ | grep cron 2>/dev/null
ls -al /etc/cron* 2>/dev/null
cat /etc/cron* 2>/dev/null
cat /etc/at.allow 2>/dev/null
cat /etc/at.deny 2>/dev/null
cat /etc/cron.allow 2>/dev/null
cat /etc/cron.deny 2>/dev/null
cat /etc/crontab 2>/dev/null
cat /etc/anacrontab 2>/dev/null
cat /var/spool/cron/crontabs/root 2>/dev/null


# find all writable dirs
#find / -type d \( -perm -g+w -or -perm -o+w \) -exec ls -adl {} \; 2>/dev/null

# find all suid binaries
#find / -perm -4000 -exec ls -la {} \; 2>/dev/null
