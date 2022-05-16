Get the fingerprint of a PGP public key:

```bash
gpg --with-subkey-fingerprint gpgpub.txt
```

```bash
gpg --with-fingerprint gpgpub.txt
```

Verify a signed message:

```bash
gpg --verify sig.txt
```

Encrypt a file with a passphrase (this generates a .gpg file):

```bash
gpg -c plain.txt
```

Decrypt a file with a passphrase:

```bash
gpg -o decrypted.txt --decrypt plain.txt.gpg
```

Export a public key:

```bash
gpg --export -a --output pubkey.txt
```

Export a private key:

```bash
gpg -a --export-secret-keys > privkey.txt
```
