## General Information

- https://fadedlab.wordpress.com/2017/07/25/searching-ldap-using-nmaps-ldap-search-nse/

`LDAP (Lightweight Directory Access Protocol)` is a software protocol for enabling anyone to locate organizations, 
individuals, and other resources such as files and devices in a network, whether on the public Internet 
or on a corporate intranet. LDAP is a "lightweight" (smaller amount of code) version of Directory Access Protocol (DAP).

An LDAP directory can be distributed among many servers. 
Each server can have a replicated version of the total directory that is synchronized periodically. 
An LDAP server is called a Directory System Agent (DSA). 

An LDAP server that receives a request from a user takes responsibility for the request, 
passing it to other DSAs as necessary, but ensuring a single coordinated response for the user.

`LDAP Data Interchange Format LDIF` (LDAP Data Interchange Format) defines the directory content as a set of records. 
It can also represent update requests (Add, Modify, Delete, Rename).


## Enumerating an LDAP service 

### Connecting without credentials 

```python
#!/usr/bin/env python3
import ldap3

ip = "192.168.243.136" 
port = 389 
use_ssl = False
server = ldap3.Server(host=ip, port=port, use_ssl=use_ssl, get_info='ALL') 
connection = ldap3.Connection(server=server, auto_bind=True) 
print(server.info)
```

### Getting all objects in a directory

```python
#!/usr/bin/env python3
connection = ldap3.Connection(server=server, auto_bind=True)
```

### Dumping the whole LDAP

```python
connection.search(search_base='DC=DOMAIN,DC=DOMAIN', search_filter='(&(objectClass=person))', search_scope='SUBTREE', attributes='userPassword')
```

### Reading all the public information 

```bash
nmap -Pn -n -p389 -sV --script "ldap* and not brute" $IP ldapsearch -LLL -Wx -b "dc=nodomain" -h $IP
```