## Configuring the command-line interface

First, register here:

 - https://aws.amazon.com/

Then, create a new IAM and an API key.

### Installing and authenticating

- https://github.com/aws/aws-cli

```bash
apt install awscli
```

Provide your access key id, access key secret and the region name.
You can use an example region: `eu-central-1`.

```bash
aws configure
```

## Using the S3 buckets API

Creating a S3 buckets:

```bash
aws s3 mb s3://kommandos
aws s3api create-bucket --acl private --region eu-central-1 --bucket kommandos --create-bucket-configuration LocationConstraint=eu-central-1
```

Listing S3 buckets:

```bash
aws s3 ls
```

Deleting an S3 bucket:

```bash
aws s3 rb s3://kommandos --force
```

Deleting a file from a S3 bucket:

```bash
aws s3 rm s3://kommandos/w00t.txt
```

Listing an S3 bucket:

```bash
aws s3 ls woman-ml
```

Downloading a file from a S3 bucket:

```bash
aws s3 cp s3://woman-ml/woman.txt ./
```

Uploading a file to a S3 bucket:

```bash
aws s3 cp w00t.txt s3://kommandos/w00t.txt
```

Getting a public URL to a file from a S3 bucket:

```bash
// aws s3 presign s3://kommandos/w00t.txt --expires-in 600
aws s3api put-object-acl --bucket kommandos --acl public-read --key w00t.txt
```


## Using Route 53 DNS services

Listing hosting zones:

```bash
aws route53 list-hosted-zones
```

Getting information about a hosting zone:

```bash
aws route53 get-hosted-zone --id /hostedzone/<zone_id>
```

## Updating DNS records

Creating or updating DNS record sets:

```bash
aws route53 change-resource-record-sets --hosted-zone-id /hostedzone/Z00860311Z1Z6UDR5DYPQ --change-batch file://aws-route53-configuration.json

{
  "Comment": "Create or update the A record set ",
  "Changes": [
    {
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "example.com",
        "Type": "A",
        "TTL": 300,
        "ResourceRecords": [
          {
            "Value": "10.0.10.10"
          }
        ]
      }
    }
  ]
}
```

## Using EC2

Listing EC2 instances:

```bash
aws ec2 describe-instances
```

Listing running instances:

```bash
aws ec2 describe-instances --filters Name=instance-state-name,Values=running
aws ec2 describe-instances --filters Name=instance-state-name,Values=running --query 'Reservations[*].Instances[*].[InstanceId,InstanceType,KeyName,PublicIpAddress]' --output text
```

Viewing the given instance:

```bash
aws ec2 describe-instances --instance-id <instance-id>
```

Choosing an image:

```bash
aws ec2 describe-images --owners amazon --filters "Name=platform,Values=windows"
aws ec2 describe-images --owners amazon --filters "Name=platform,Values=windows" --query "Images[*].[ImageId,State,Description]"
aws ec2 describe-images --owners amazon --filters "Name=name,Values=*ubuntu*server*" --query "Images[*].[ImageId,Description,PlatformDetails]"
aws ec2 describe-images --owners amazon --filters "Name=name,Values=Ubuntu*20.04*" --query "Images[*].[ImageId,Description,PlatformDetails]"
```

### SSH keys

Getting all SSH keys:

```bash
aws ec2 describe-key-pairs
aws ec2 describe-key-pairs --query "KeyPairs[*].[KeyName,KeyPairId]" --output text
```

Creating a new SSH key:

```bash
aws ec2 create-key-pair --key-name proxy-key
```

Creating a new SSH key and saving it to a file:

```bash
aws ec2 create-key-pair --key-name <key_name>
key_name="proxy-key"; aws ec2 create-key-pair --key-name $key_name |jq '.KeyMaterial' |sed 's/\\n/\n/g' |sed 's/"//g' > $key_name
```

Deleting an SSH key:

```bash
aws ec2 delete-key-pair --key-name proxy-key
```

### Listing firewall rules (security groups):

Getting all security groups:

```bash
aws ec2 describe-security-groups
```

### Starting a new instance

Starting an instance with default settings:

```bash
aws ec2 run-instances --image-id <image-id>
```

Starting an instance with the given security group and the ssh key:

```bash
aws ec2 run-instances --image-id ami-0746eb3cb5c684ae6 --key-name proxy-key --security-group-ids sg-0fb4d9f16681519ea --instance-type t2.micro
```

Starting an instance with the given security group, the ssh key and the name:

```bash
aws ec2 run-instances --image-id ami-0746eb3cb5c684ae6 --key-name proxy-key --security-group-ids sg-0fb4d9f16681519ea --instance-type t2.micro --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=My-Awesome-Instance}]'
```

### Terminating an instance

```bash
aws ec2 terminate-instances --instance-id <instance-id>
```
