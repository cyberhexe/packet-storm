## Tar files

Tar files or folders:

```bash
tar czf Atutor.tar.gz Atutor/
```

## Networking

Invoking scripts on interface creation:

```bash
# cat /etc/network/if-up.d/huawei-network

#! /bin/sh
# Remove the default route added by the Huawei modem when it shows up

set -e

# Only run from ifup.
if [ "$MODE" != start ]; then
	exit 0
fi

if [ "$IFACE" = eth1 ]; then
    ip ro del default via 192.168.8.1 dev eth1 proto dhcp src 192.168.8.100 metric 100 
    ip ro add 10.10.10.10 via 192.168.8.1 dev eth1 proto dhcp src 192.168.8.100 metric 100
    ip ro add 10.10.10.12 via 192.168.8.1 dev eth1 proto dhcp src 192.168.8.100 metric 100
fi
```

## APT Commands

Using APT with a proxy:

- https://askubuntu.com/a/257296

```bash
echo ‘Acquire::http::Proxy "socks5h://127.0.0.1:4200";’ > /etc/apt/apt.conf.d/11-proxy
apt update
```

## Docker Commands

### Setting a proxy for running containers

Create a configuration file:

```bash
mkdir -p ~/.docker/
touch ~/.docker/config.json
```

Add the following content to the `config.json` file:

```json
{
 "proxies":
 {
   "default":
   {
     "httpProxy": "socks5h://127.0.0.1:4200",
     "httpsProxy": "socks5h://127.0.0.1:4200",
     "noProxy": "127.0.0.0/8"
   }
 }
}
```


Building Docker images for a different architecture:

```bash
docker buildx build --load --builder generic-builder --platform linux/arm64 -f ./Dockerfile -t masscan-web-ui-docker-arm64
```

Saving an image to a file:

```bash
docker save image-name > image.tar
```

Loading an image from a file:

```bash
docker load image-name < image.tar
```

## Docs/Notes Convertation

Exporting Cherrytree notes in bash:

```bash
#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <ctb file> <output directory>"
    exit 0
fi

if [ -z "$2" ]; then
    echo "Usage: $0 <ctb file> <output directory>"
    exit 0
fi

ctb_file="$1"
output_dir="$2"

echo "Converting $ctb_file"

xvfb-run -s '-terminate' cherrytree -t . "$ctb_file" &&
mv "$ctb_file"_TXT "$output_dir" &&
echo OKAY
```

### Reading JSON in Bash

Extracting a JSON array and looking for matches:

```bash
curl http://localhost:8090/burp/scanner/issues | jq -r '.issues[] | select(.severity=="Low").url' > /tmp/findings.txt
```

### Downloading files recursively

Using wget:

```bash
wget -r -np -k http://192.168.178.22:5000/
```

### Replacing content with sed

Substitution from env variables:

```bash
cat microsocks.service|sed -e "s|MICROSOCKS_IP|$MICROSOCKS_IP|"
```

### Searching for content

Using grep:

```bash
grep -rnwi "function addattachment" /usr/local/atmail --color=auto>/dev/null
grep -r globalsave *
grep -rnw /var/www/html/ATutor/ -e “^.*user_location.*public.*” --color
grep -rnw /var/www/html/ATutor/ -e “function searchFriends” --color
egrep '\$addslashes.*=.*' /var/www/html/ATutor/ -r --color
egrep -r "define\('MYSQL" /var/www/html/ATutor/ --color
grep -ir  "IMS manifest file is missing" /var/www/html/ATutor
grep -rnw "eval(" . --color
```

### Encoding data

HEX to ASCII:

```bash
echo "7069 7a64 6176 6167 696e 610a" |xxd -r -p
```

ASCII to HEX

```bash
echo “pizdavagina”|xxd
```

### Networking

Forwarding ports with iptables:

```bash
#!/bin/bash

P_src=443
P_target=80

echo "1" > /proc/sys/net/ipv4/ip_forward

iptables -t nat -A PREROUTING -s 127.0.0.1 -p tcp --dport $P_src -j REDIRECT --to $P_target
iptables -t nat -A OUTPUT -s 127.0.0.1 -p tcp --dport $P_src -j REDIRECT --to $P_target
```

Mounting a remote filesystem via ssh:

```bash
sudo sshfs -o IdentityFile=kommandos-key.pem gh0st@10.10.10.10:/home/gh0st/huginn /mnt
```

### Storing credentials locally

Configuring git to store credentials securely:

```bash
#!/bin/bash
set - e
sudo apt-get -y install libsecret-1-0 libsecret-1-dev libglib2.0-dev
sudo make --directory=/usr/share/doc/git/contrib/credential/libsecret
git config --global credential.helper /usr/share/doc/git/contrib/credential/libsecret/git-credential-libsecret
```
