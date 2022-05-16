## General Information

### What's a honeypot what what it’s purpose?

It’s a computer or Virtual Machine emulating some services (ex:  SSH, FTP, Telnet, Netbios, HTTPS, a Samba server, etc) and accepting, logging and sending warnings of all incoming connections.

You can use it for intrusion detection or for doing initial warning but it also might go a little further and allow one to get inside the intruders ”head” since you get to log every interaction.

### How and where should it be placed?

Starting with "where". They are usually deployed in specific areas to get an idea how/or if the network is tested from outside or inside.
So there are three major areas; behind firewalls, in “sensible zones” where only predefined machines should have access to and in the “public zone” such as administrative/general network.

Placing a honeypot behind firewalls/"sensible zones" will ensure that the firewall is doing it’s job and if you get a hit that means you have a miss-configurations or a serious trouble.

Honeypots placed in the "public zone" will give you a glimpse if you have someone skimming your network.

### How to place it?

This answer can be split in two parts, hardware and timeline.
* vCPU and 512 RAM will be enough for each instance.
* Deploying the honeypots from the most to the least secure zones in the network is recommended. In the most secure zone you should have no events at all where as in the least you might get a couple, his approach will give some time to understand eventual breaches and mature responses. (opposite to having lots of hits all across the network and spreading resources in order to understand what’s happening)

## Deploying a Honeypot with Nepenthes

Nepenthes runs on a variety of operating systems, including Windows via Cygwin, Mac OS X, Linux, and BSD.

### Installing Nepenthes

To get started with the installation, type the following command:

```bash
sudo apt-get install nepenthes
```

This will install nepenthes and add the user account and group (both named nepenthes) that the daemon process runs as.

Once the package is installed, you can start nepenthes as a service with the following command.

```bash
sudo service nepenthes start
```

When nepenthes begins running, it binds to several ports on your system.
These are the ports on which nepenthes expects to see common remote exploitation.

To receive connections on these ports from machines on the Internet, you must allow access to the ports through any firewalls on your network.

Also, if you are dropping or restricting traffic to your system with iptables (a host-based firewall), you can use the
following command to open access to the ports required by nepenthes.

```bash
sudo iptables -I INPUT -p tcp --dport <port_number> -j ACCEPT
```

## Deploying a Honeypot With OpenCanary

A very simple honeypot is opencanary. 
It's freeware, it emulates Windows/Linux server, as well as a Mysql server, FTP, SSH, etc.

Configuration samples:
- https://hackernoon.com/how-to-deploy-honeypots-in-your-network-91fe428d43fd

### Installing OpenCanary

First, install Ubuntu server version and make all the security updates.

Install necessary libs and the honeypot

```bash
sudo apt-get install python-dev python-pip python-virtualenv
virtualenv env/
. env/bin/activate
pip install opencanary
sudo apt-get install -y build-essential libssl-dev libffi-dev python-dev
pip install rdpy
```


Run it

```bash
. env/bin/activate
opencanaryd --copyconfig
opencanaryd --start
```