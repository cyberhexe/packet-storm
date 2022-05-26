## Sniffing with tcpdump

Sniffing everything:

```bash
tcpdump -i lo
```

Sniffing on the specific port

```bash
tcpdump -i lo port 25
```


### Sniffing HTTP traffic

Showing only HTTP traffic with headers and message body

```bash
tcpdump -i any -A -s 0 'tcp port 8090 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'
```

Showing only HTTP traffic with headers and message body from a particular source
```bash
tcpdump -i any -A -s 0 'src example.com and tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'
```


## Sniffing with tcpflow

Sniffing on the specific port
```bash
tcpflow -c port 25
```

Showing data as HEX

```bash
tcpflow -c port 25 -D
```

## Sniffing with tshark

Extracting all outgoing IP addresses

```bash
tshark -r darksouls.pcapng -Y "ip.dst_host != 192.168.178.43" -T fields -e ip.dst_host |sort |uniq
```

## Sniffing with bettercap

Starting bettercap with a web server

```bash
bettercap -iface tun0 -caplet https-ui
```

Hijacking HTTPS connections

```bash
bettercap -iface tun0 -caplet https-ui -caplet hstshijack/hstshijack.cap
```

## Sniffing with Metasploit 

Using Meterpreter sniffer

```bash
meterpreter > use sniffer
meterpreter > sniffer_interfaces
meterpreter > sniffer_start 2
meterpreter > sniffer_dump 2 /tmp/all.cap
```

Meterpreter - packetrecorder

```bash
meterpreter > run packetrecorder 
meterpreter > run packetrecorder -li
meterpreter > run packetrecorder -i 2 -l /root/
root@kali:~/logs/packetrecorder/XEN-XP-SP2-BARE_20101119.5105# tshark -r XEN-XP-SP2-BARE_20101119.5105.cap |grep PASS
```

## Sniffing serial ports

- https://github.com/nochkin/interceptty                                                       
- https://github.com/snarlistic/jpnevulator                                                    

