### Resolving DNS records 

Resolving name servers 

```bash
host -t ns megacorpone.com 
# resolve NS addresses
for ns in $(host -t ns megacorpone.com |cut -d" " -f4); do 
    host -t a $ns |cut -d" " -f4
done
```

### Resolving MX records 

```bash
host -t mx megacorpone.com
```

### Resolving TXT records 

```bash
dig -t txt megacorpone.com
```

### Resolving all available records with DNSRecon 

```bash
dnsrecon -d megacorpone.com -t avfr
```

## Zone transfers 

A zone transfer can be compared to a database replication act between related DNS servers. 
The process includes the copying of one zone file from a master server to a secondary server. 
The Zone File contains a list of all the DNS names configured for that zone. 
For this reason, Zone Transfers should usually be limited to authorized secondary DNS servers only.

### Requesting a zone transfer 

```bash
nmap --script=dns-zone-transfer -p 53 ns2.megacorpone.com
```

```bash
host -t ns megacorpone.com 
host -l megacorpone.com ns2.megacorpone.com.
```

## Enumerating DNS servers 

### Enumerating with dnsenum 

```bash
dnsenum zonetransfer.me
```

### Enumerating with aiodnsbrute 

- https://github.com/blark/aiodnsbrute 

```bash
aiodnsbrute --wordlist /usr/share/seclists/Discovery/DNS/namelist.txt --resolver-file resolvers-ips.txt example.org | tee aiodnsbrute-lookup.txt
```

### Gathering domain names with DNS Zone Transfers and certificate grabbing 

```bash
amass enum -d example.org -src
```

### Gathering domain names with DNS Zone Transfers, certificate grabbing and subdomains bruteforcing 

```bash
amass enum -active -ip -d example.com -src -brute
```
