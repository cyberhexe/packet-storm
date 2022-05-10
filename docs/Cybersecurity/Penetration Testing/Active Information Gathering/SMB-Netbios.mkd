## Enumerating NetBIOS services 

The SMB Netbios service listens on the `445/tcp` port. 
It is also available through `139/tcp` port. 
A list to clarify SMB version numbers, and their related Windows Operating system versions: 
- SMB1 - Windows 2000, XP and Windows 2003. 
- SMB2 – Windows Vista SP1 and Windows 2008 
- SMB2.1 – Windows 7 and Windows 2008 R2 
- SMB3 – Windows 8 and Windows 2012

### Scanning a network with Nbtscan 

```bash
nbtscan 10.11.1.0/24
```

### Scanning a network with Metasploit 

```bash
msf > use auxiliary/scanner/netbios/nbname 
msf auxiliary(nbname) > set RHOSTS 192.168.1.200-210 
msf auxiliary(nbname) > set THREADS 11 
msf auxiliary(nbname) > run
```

## Enumerating SMB services 
### Scanning a network with Metasploit 

```bash
msf > use auxiliary/scanner/smb/smb_version 
msf auxiliary(smb_version) > setg RHOSTS 10.11.1.1-254 
msf auxiliary(smb_version) > setg THREADS 10 
msf auxiliary(smb_version) > run
```

### Finding nmap SMB scripts 

```bash
locate smb |grep nse |grep nmap |grep scripts |xargs grep categories
```

### Finding exposed SMB services 

```bash
nmap -p139,445 10.11.1.0/24 --open
```

### Logging in to SMB services with credentials 

```bash
msf > use auxiliary/scanner/smb/smb_login 
msf auxiliary(smb_login) > set RHOSTS 192.168.1.0/24 
msf auxiliary(smb_login) > set SMBUser victim 
msf auxiliary(smb_login) > set SMBPass s3cr3t 
msf auxiliary(smb_login) > set THREADS 50 
msf auxiliary(smb_login) > run
```

## Reading and writing to network shares 
### Mounting remote share over network 

```bash
sudo mount -t cifs //$IP/ITDEPT /mnt -o user=dawn
```

```bash
sudo smbmount "\\$IP\ITDEPT" /mnt -o user=dawn
```

### Getting files from shares 

```bash
smbmap -H 192.168.59.11 smbmap -H $IP -R
```

```bash
/usr/bin/smbclient "\\$IP\ITDEPT" --user dawn dawnpassword
```

### Uploading files to shares 

```bash
curl smb://192.168.59.11:445/ITDEPT/test.txt -T test.txt curl -u "DAWN/dawn:dawn" --upload-file pwn.sh "smb://$IP/ITDEPT/"
```

## Enumeration 

A null session refers to an unauthenticated NetBIOS session between two computers. 
This feature exists to allow unauthenticated machines to obtain browse lists from other Microsoft servers.

A null session also allows unauthenticated hackers to obtain large amounts of information about the machine, 
such as password policies, usernames, group names, machine names, user and host SIDs. 
This Microsoft feature existed in SMB1 by default and was later restricted in subsequent versions of SMB.

### Discovering open pipes

```bash
msf> use auxiliary/scanner/smb/pipe_auditor
```

### Logging in without credentials 

```bash
rpclient -U "" 10.11.1.8
```

### Using nmblookup
```bash
nmblookup
```

### Enumerating system properties 

```bash
rpcclient $> srvinfo
```

### Enumerating system users 

```bash
rpcclient $> enumdomusers
```

### Enumerating password policies 

```bash
rpcclient $> getdompwinfo
```

### Enumerating network shares 

```bash
rpcclient $> netshareenum
```

### Enumerating the user's SID 

```bash
rpcclient $> lookupnames root
```

### Enumerating privileges 

```bash
rpcclient $> enumprivs
```

### Getting user data with a SID 

```bash
rpcclient $> lookupsids S-1-5-21-1086716168-3792659489-4186792627-1000
```

### Using nmap with NULL session 

```bash
nmap -p139,445 --script smb-enum-users 10.11.1.24
```

### Running enum4linux 

```bash
enum4linux -v 10.11.1.24
```

### SMB vulnerability scan 

```bash
nmap -p139,445 --script vuln --script-args=unsafe=1 10.11.1.24
```
