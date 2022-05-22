## Enumerating Wordpress 

##Using wpscan:

Running a basic scan:

```bash
wpscan --url "http://dc-2/"
```

Enumerating plugins and databases:

```bash
export URL="https://example.com"
wpscan --url "$URL" --api-token --enumerate dbe
```

Checking available XMLRPC methods:

```http
POST /xmlrpc.php HTTP/1.1
Host: dc-2
Upgrade-Insecure-Requests: 1
Connection: close
Content-Type: application/xml
Content-Length: 91

<methodCall>
<methodName>system.listMethods</methodName>
<params></params>
</methodCall>
```

