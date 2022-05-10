## Reading X509 certificates 

Reading PKCS12 certificates 

```bash
openssl pkcs12 -in QWAC1.p12 -nodes -passin pass:"1111" |openssl x509 -noout -text
```

Reading X509 certificate 

```bash
openssl x509 -in cert.pem -noout -text
```

## Generating X509 certificate 

Generating a new certificate in the PEM format 

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```