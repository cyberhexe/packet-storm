Create a new container filled with zeros:

```bash
dd if=/dev/zero of=encrypted.img bs=1 count=0 seek=300MB
```

Encrypt the container with LUKS:

```bash
sudo cryptsetup luksFormat encrypted.img
```

Unlock the container:

```bash
sudo cryptsetup luksOpen encrypted.img <volume_name>
```

Create a ext4 filesystem inside the container:

```bash
sudo mkfs.ext4 /dev/mapper/<volume_name>
```

Mount the container:

```bash
sudo mount /dev/mapper/<volume_name> /mnt
```

Lock the container:

```bash
sudo umount /mnt
sudo cryptsetup luksClose <volume_name>
```
