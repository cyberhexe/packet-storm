### Performing network discovery

Probing IPv6 neighbor solicitations:

```bash
msf > use auxiliary/scanner/discovery/ipv6_neighbor
msf auxiliary(ipv6_neighbor) > set RHOSTS 192.168.1.2-254
msf auxiliary(ipv6_neighbor) > set SHOST 192.168.1.101
msf auxiliary(ipv6_neighbor) > set SMAC d6:46:a7:38:15:65
msf auxiliary(ipv6_neighbor) > set THREADS 55
msf auxiliary(ipv6_neighbor) > run</p>
```

Probing common UDP services:

```bash
msf > use auxiliary/scanner/discovery/udp_probe
msf auxiliary(udp_probe) > set RHOSTS 192.168.1.2-254
msf auxiliary(udp_probe) > set THREADS 253
msf auxiliary(udp_probe) > run</p>
```

```bash
msf > use auxiliary/scanner/discovery/udp_sweep
msf auxiliary(udp_sweep) > set RHOSTS 192.168.1.2-254
msf auxiliary(udp_sweep) > set THREADS 253
msf auxiliary(udp_sweep) > run</p>
```