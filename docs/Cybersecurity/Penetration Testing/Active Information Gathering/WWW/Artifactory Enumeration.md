## Artifactory Enumeration

Resources:

- https://www.errno.fr/artifactory/Attacking_Artifactory

By default, no password locking policy is in place which makes Artifactory a prime target for credential stuffing and password spraying attacks.

### Checking accounts rights 

```bash
curl http://localhost:8081/artifactory/ui/repodata?deploy=true
```

### Getting the artifactory version

```bash
curl /ui/api/v1/system/status/nodes
```

### Getting information about the current user 

```bash
curl /ui/api/v1/ui/auth/current HTTP/1.1
```
