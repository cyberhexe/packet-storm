## Collecting evidence with auditd

- https://capsule8.com/blog/auditd-what-is-the-linux-auditing-system/

Installing auditd:

```bash
#!/bin/bash
apt-get install auditd
auditctl -a task,always
ausearch -i -sc execve
```
