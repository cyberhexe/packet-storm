## Enumerating RPC services

```bash
nmap -sR 10.11.1.237
```

### rpcinfo

#### Querying all registered RPC programs 

```bash
rpcinfo -p 10.11.1.237
```

### Making an RPC call to the specified port 

```bash
rpcinfo -n 2049 10.11.1.72
```

### Displaying RPC bind stats 

```bash
rpcinfo -m 10.11.1.72
```

### Displaying registered RPC programs 

```bash
rpcinfo -s 10.11.1.72
```

### Displaying all entries of the given prognum 

```bash
rpcinfo -l 10.11.1.72 100000 2
```

## Enumerating DCERPC services
### Querying the endpoint mapper service 

```bash
msf > use auxiliary/scanner/dcerpc/endpoint_mapper 
msf auxiliary(endpoint_mapper) > set RHOSTS 192.168.1.200-254
msf auxiliary(endpoint_mapper) > set THREADS 55 
msf auxiliary(endpoint_mapper) > run
```

### Locating hidden RPC services 

```bash
msf > use auxiliary/scanner/dcerpc/hidden 
msf auxiliary(hidden) > set RHOSTS 192.168.1.200-254 
msf auxiliary(hidden) > set THREADS 55 
msf auxiliary(hidden) > run
```

### Obtaining information from the DCERPC services 

```bash
msf > use auxiliary/scanner/dcerpc/management 
msf auxiliary(management) > set RHOSTS 192.168.1.200-254 
msf auxiliary(management) > set THREADS 55 
msf auxiliary(management) > run
```

### Scanning the network to find available DCERPC services over TCP 

```bash
msf > use auxiliary/scanner/dcerpc/tcp_dcerpc_auditor 
msf auxiliary(tcp_dcerpc_auditor) > set RHOSTS 192.168.1.200-254 
msf auxiliary(tcp_dcerpc_auditor) > set THREADS 55 
msf auxiliary(tcp_dcerpc_auditor) > run
```

