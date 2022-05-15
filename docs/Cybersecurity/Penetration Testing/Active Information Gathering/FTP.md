### Listing remote files 

```bash
curl ftp://anonymous:""@192.168.101.107:21/
```

### Downloading remote files matching pattern

```bash
wget ftp://anonymous:""@192.168.101.107:21/*.zip
```

### Checking hidden folders

```bash
ftp> ls -la
```