### Enumerating WebDAV services

The WebDAV1 protocol provides a framework for users to create, change and move documents on a server.

### Using webdav_scanner from metasploit

```bash
msf > use auxiliary/scanner/http/webdav_scanner
msf auxiliary(webdav_scanner) > setg RHOSTS 10.11.1.1-254
msf auxiliary(webdav_scanner) > setg THREADS 10
msf auxiliary(webdav_scanner) > run</p>
```

### Using the davtest tool

```bash
davtest -url http://humble.thinc.local
```
