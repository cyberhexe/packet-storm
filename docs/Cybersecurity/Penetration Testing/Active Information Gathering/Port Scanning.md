### Searching for open ports 

Displaying scanned services with metasploit 

```bash
msf > services -p 22 -c name,port,proto Services
host name port proto
172.16.194.163 ssh 22 tcp 172.16.194.172 ssh 22 tcp
```

```bash
msf > services -p 21 -c name,proto Services
host name proto
172.16.194.172 ftp tcp
```

### Sweeping ports 

```bash
nmap -p 80 10.11.1.0/24 -oG web-sweep-nmap grep Ports web-sweep-nmap |grep open |cut -d" " -f2
```

### Scanning ports 

Running TCP connect scan with the number of ports limited to 20 

```bash
nmap -sT --top-ports 20 10.11.1.0/24 -oG top-ports-nmap cat top-ports-nmap |grep 21/open |cut -d" " -f2
```

Grabbing the banner 

```bash
nmap -sV -O 10.11.1.8 nmap -A 10.11.1.8
```

Scanning UDP 

```bash
nc -nv -u -z -w 1 10.0.0.19 160-162 (UNKNOWN) [10.0.0.19] 161 (snmp) open
```

### Scanning with Metasploit

Using nmap with a Metasploit database:

```bash
msf > db_nmap -A 172.16.194.134
[*] Nmap: Starting Nmap 5.51SVN ( http://nmap.org ) at 2012-06-18 12:36 EDT
[*] Nmap: Nmap scan report for 172.16.194.134
[*] Nmap: Host is up (0.00031s latency).
```
