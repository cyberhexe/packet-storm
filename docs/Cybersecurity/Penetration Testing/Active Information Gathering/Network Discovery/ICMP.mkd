## Ping discovery

### Sweeping the network with fping

```bash
#!/bin/bash
if [ -z "$1" ]; then
  echo "Usage: $0 "
  echo "Example: $0 192.168.178.0/24"
  exit 1
fi
RANGE="$1"
fping -g $RANGE
```

### Sweeping the network with nmap

```bash
nmap -sn 10.11.1.0/24 -oG ping-sweep-nmap
grep Up ping-sweep-nmap |cut -d" " -f2
```
