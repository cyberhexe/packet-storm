## Profiling with recon-ng

Using the profiler module:

```bash
[recon-ng][default] > marketplace install profiler
[recon-ng][default] > modules load profiler
[recon-ng][default][profiler] > options set SOURCE target_username
[recon-ng][default][profiler] > run
```

Getting employee names and email addresses:

```bash
[recon-ng][default] > marketplace install recon/domains-contacts/whois_pocs
[recon-ng][default] > modules load recon/domains-contacts/whois_pocs
[recon-ng][default][xssed] > options set SOURCE cisco.com
[recon-ng][default][xssed] > run
```