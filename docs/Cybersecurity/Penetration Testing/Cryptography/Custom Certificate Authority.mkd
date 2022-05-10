## Creating CA keys 

Generating the CA asymmetric keys 

```bash
openssl req -x509 -new -nodes -keyout root_ca.key -sha256 -days 1024 -out root_ca.crt -subj "/C=DE/ST=Bayern/L=Muenchen/O=Speed GmbH/CN=example.com"
```

Using the CA to sign another key 

```bash
openssl req -new -nodes -keyout client.key -sha256 -days 1024 -out client.csr -subj "/C=DE/ST=Bayern/L=Muenchen/O=Speed GmbH/CN=example.com"
```

## Adding a custom root CA certificate to Kali Linux Certificate Store

Open the proxy address in your browser and download the CA certificate by clicking on the top-right button.

Convert it to the X509 format: 

```bash
openssl x509 -in cacert.der -inform DER -out ca-burp.crt
```

Copy it into the certificate store: 

```bash
sudo cp ca-burp.crt /usr/local/share/ca-certificates/
``` 

Update the certificates store: 

```bash
sudo update-ca-certificates
```

## Removing the root CA certificate from the Kali Linux Certificate Store 

Delete the certificate:

```bash
rm -rf /usr/local/share/ca-certificates/ca-burp.crt
```

Update the certificates store: 

```bash
sudo update-ca-certificates --fresh
```
