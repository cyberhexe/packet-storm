## Enumerating SMTP services 

Mail servers can also be used to gather information about a host or network. 
SMTP supports several important commands, such as `VRFY` and `EXPN`. 
A `VRFY` request asks the server to verify an email address, 
while `EXPN` asks the server for the membership of a mailing list.

- `DATA` - Defines information as the data text of themail body 
- `EHLO` - Identifies the domain name of the sending host to SMTP 
- `HELO` - Identifies the domain name of the sending host to SMTP 
- `EXPN` - Verifies whether a mailbox exists on the localhost 
- `HELP` - Provides help with SMTP commands 
- `VRFY` - Verifies whether a mailbox exists on the localhost

### Verifying if a user exists 

```bash
nc -nvv 10.11.1.128 25 
220
VRFY bob 
250 2.5.1 bob@domain.local
```

### Verifying if a user exists with smtp-user-enum 

```bash
smtp-user-enum -M VRFY -u root -t $IP
```

### Enumerating users on the server 

```bash
for user in $(cat users.txt);do 
  echo VRFY $user |nc -nvv -w 1 "$IP" 25 2>/dev/null |grep ^"250"; 
done
```