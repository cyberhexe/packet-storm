## Querying Shodan database

Locating exposed Kibana servers

```text
kibana content-length: 217
```

Find all devices on the Internet from San Diego:

```text
city:"San Diego"
```

Exclude all devices from San Diego:

```text
-city:"San Diego"
```

Find all services running on ports 23,1023:

```text
port:23,1023
```

Find all devices on with port 8080 opened where the main text banner isn't empty:

```text
port:8080 -hash:0
```

Find all services by the given product (exclude port 22):

```text
product:openssh -port:22
```

## Using Shodan CLI

Searching Microsoft IIS servers:

```bash
shodan search --fields ip_str,port,org,hostnames microsoft iis 6.0
```

Getting facets for a search query

```text
shodan stats --facets country apache
```

