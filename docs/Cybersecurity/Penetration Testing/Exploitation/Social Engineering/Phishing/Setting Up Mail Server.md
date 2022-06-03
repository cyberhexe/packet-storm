## Starting a simple python SMTP server

```bash
python3 -m smtpd -n -c DebuggingServer 0.0.0.0:25
```

## Cleaning up remote email box

```bash
#!/usr/bin/env python3

import imaplib
import sys

if len(sys.argv) != 2:
    print(f"(+) usage: {sys.argv[0]} <target>")
    sys.exit(-1)

atmail = sys.argv[1]

print(f"Cleaning up {atmail}")

box = imaplib.IMAP4(atmail, 143)
box.login("admin@offsec.local", "123456")
box.select('Inbox')

typ, data = box.search(None, 'ALL')

for num in data[0].split():
    box.store(num, '+FLAGS', '\\Deleted')

box.expunge()
box.close()
box.logout()
print('Done')
```
