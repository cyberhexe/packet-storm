## Hosting servers on Digital Ocean

First, get yourself registered here:

- https://cloud.digitalocean.com/

Then, create an API key:

 - https://cloud.digitalocean.com/account/api/tokens

Finally, upload your SSH public key:
 - https://cloud.digitalocean.com/account/security

### Using command-line interface

Installing and authenticating
- https://docs.digitalocean.com/reference/doctl/how-to/install/

```bash
snap install doctl
doctl auth init
doctl account get
```

### Using the Digital Ocean API:

Listing available regions:

```bash
doctl compute region list
```

Listing available instance capacities:

```bash
doctl compute size list
```

Listing active droplets:

```bash
doctl compute droplet list
```

Listing all available droplet sizes:

```bash
doctl compute size list
```

Instantiating a new droplet:

```bash
doctl compute droplet create --image ubuntu-20-04-x64 --size s-1vcpu-1gb --region fra1 <droplet_name>
```

Instantiating a new droplet and specifying the ssh-key fingerprint:

```bash
doctl compute droplet create --image ubuntu-20-04-x64 --size s-1vcpu-1gb --region fra1 <droplet_name> --ssh-keys
```

Deleting droplets:

```bash
doctl compute droplet delete <droplet_name>
```