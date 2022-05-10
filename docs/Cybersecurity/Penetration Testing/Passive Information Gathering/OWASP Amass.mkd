## Gathering intel with Amass

Performing certificate grabbing:

```bash
amass intel -active -addr 10.10.10.10
```

Grabbing certificates from an IP range:

```bash
amass intel -addr 10.10.10.0-254 -active
```

Gathering ASN assigned to an organization:

```bash
amass intel -org 'Apple'
```

Gathering domains and Whois information:

```bash
amass intel -d offensive-security.com -whois
```

Gathering domain names without DNS resolution

```bash
amass enum -passive -d example.org -src
```
