Enumerating TLS encryption ciphers used by a website 

```bash
#!/usr/bin/env bash

SERVER=$1
DELAY=1
ciphers=$(openssl ciphers 'ALL:eNULL' | sed -e 's/:/ /g')

for cipher in ${ciphers[@]}; do 
  echo -n Testing $cipher... result=$(echo -n | openssl s_client -cipher "$cipher" -connect $SERVER 2>&1) if [[ "$result" =~ ":error:" ]] ; then error=$(echo -n $result | cut -d':' -f6) echo NO ($error) else if [[ "$result" =~ "Cipher is ${cipher}" || "$result" =~ "Cipher :" ]] ; then echo YES else echo UNKNOWN RESPONSE echo $result fi fi sleep $DELAY 
done
```


Need to grab the server's HTTPS certificate? 

```bash
openssl s_client -servername www.example.com -connect www.example.com:443 2>/dev/null | openssl x509 -text
```


Extracting the server's certificate and saving it in the PEM format 

```bash
openssl s_client -connect www.google.com:443 2>/dev/null </dev/null | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p'
```
