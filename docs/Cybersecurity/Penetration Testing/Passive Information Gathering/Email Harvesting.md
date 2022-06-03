## Email Harvesting

Email harvesting is an effective way of finding emails, and possibly usernames, belonging to an organization. 
These emails are useful in many ways, such as providing us a potential list for client side attacks, revealing the naming convention used in the organization, or mapping out users in the organization.

### Using theharvester

```bash
theharvester -d cisco.com -b google > google.txt
theharvester -d cisco.com -l 10 -b bing > bing.txt
theHarvester -d cisco.com -b bing,google,yahoo,sublist3r -l 1000
```

### Grepping emails from text:

```bash
grep -i -o '[A-Z0-9._%+-]\+@[A-Z0-9.-]\+\.[A-Z]\{2,4\}' response.txt
```

### Using CrossLinked

- https://github.com/m8r0wn/CrossLinked

Scraping username and assembling the email list:

```bash
python3 crosslinked.py -f '{first}.{last}@domain.com' "Example GmbH" --safe
```

