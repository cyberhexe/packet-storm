Displaying the key's fingerprint 

```bash
ssh-keygen -l -f id_rsa.pub
```

Displaying the key's fingerprint in MD5 format 

```bash
ssh-keygen -E md5 -lf id_rsa.pub
```

### Generating RSA keys (public and private keys) 

Generating RSA key pair (public and private key):

```bash
openssl genrsa -out key.pem openssl rsa -in key.pem -out key.pub -pubout
```

### Encrypting/Decrypting files with RSA keys 

Encrypting a file with a public key
```bash
echo "secret_note" > pass.txt 
openssl rsautl -in pass.txt -out pass.enc -pubin -inkey key.pub -encrypt
```

Decrypting a file with a private key:

```bash
openssl rsautl -in pass.enc -out pass.dec -inkey key.pem -decrypt
```