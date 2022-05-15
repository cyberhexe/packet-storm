- https://learn.hashicorp.com/tutorials/terraform/aws-build?in=terraform/aws-get-started#prerequisites
- https://www.terraform.io/language
- https://www.terraform.io/language/resources/provisioners/remote-exec
- https://www.terraform.io/language/values/variables

## Using terraform with AWS

Installing Terraform:

- https://www.terraform.io/downloads

```bash
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install terraform
```

Download AWS CLI:

```bash
sudo apt install awscli
```

Creating Terraform configurations:

```bash
touch main.tf
```

Paste the configuration below and save the file:

```terraform
terraform {
  required_version = ">= 0.14.9"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }
}
provider "aws" {
  profile = "default"
  region  = "eu-central-1"
}

resource "aws_key_pair" "kraken-key" {
  key_name   = "kraken-key"
  public_key = "ssh-rsa AAA... 1@1"
}

resource "aws_security_group" "redform_security" {
  ingress {
    description      = "SSH from everywhere"
    from_port        = 22
    to_port          = 22
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "allow_ssh"
  }
}

resource "aws_instance" "redform_server" {
  ami           = "ami-0b1deee75235aa4bb"
  instance_type = "t2.micro"
  vpc_security_group_ids = [aws_security_group.redform_security.id]
  key_name         = "kraken-key"

  tags = {
    Name = "RedFormInstance"
  }
}

output "instance_ip" {
  description = "The public ip for ssh access"
  value       = aws_instance.redform_server.public_ip
}
```


Initializing the Terraform directory:

```bash
terraform init
```

Checking the execution plan:

```bash
terraform plan
```

Validating the configuration:

```bash
terraform validate
```

Applying and executing:

```bash
terraform apply
```

Inspecting the state:

```bash
terraform show
```

Destroying the servers:

```bash
terraform destroy
```
