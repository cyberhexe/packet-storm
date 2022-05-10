### Using NFS to gain direct host access

```bash
mount -t nfs 10.11.1.217:/ /temp -o nolock
```

### Listing available network mounts on the host

```bash
showmount -e 10.11.1.217
```
