#!/usr/bin/env python3

import os
import boto3

DEFAULT_IMAGE_ID = 'ami-0746eb3cb5c684ae6'
DEFAULT_INSTANCE_TYPE = 't2.micro'
DEFAULT_INSTANCE_NAME = 'proxy-instance'
DEFAULT_KEY_NAME = 'proxy-key'


def get_arguments():
    from argparse import ArgumentParser
    parser = ArgumentParser(description='AWS EC2 Auto-Deployment Script')
    # COMMANDS
    parser.add_argument("--start",
                        dest="start",
                        action='store_true',
                        required=False,
                        help="Start a new EC2 instance")
    parser.add_argument("--status",
                        dest="status",
                        action='store_true',
                        required=False,
                        help="Print the current stats to the console")
    parser.add_argument("--terminate-all",
                        dest="terminate_all",
                        action='store_true',
                        required=False,
                        help="Terminate all running EC2 instances")

    # ARGS
    parser.add_argument("--image-id",
                        dest="image_id",
                        required=False,
                        default=DEFAULT_IMAGE_ID,
                        type=str,
                        help="Specify the image id to use while creating an instance. "
                             f"Default is {DEFAULT_IMAGE_ID} (Ubuntu 20.04).")
    parser.add_argument("--key-pair-name",
                        dest="key_pair_name",
                        required=False,
                        default=DEFAULT_KEY_NAME,
                        type=str,
                        help="Specify the key pair name to use alongside the created instance. "
                             f"Default is {DEFAULT_KEY_NAME}")
    parser.add_argument("--force-recreate-key",
                        dest="force_recreate_key",
                        action='store_true',
                        required=False,
                        help="Recreate the SSH key if already exists")
    parser.add_argument("--security-group-id",
                        dest="security_group_id",
                        required=False,
                        type=str,
                        help="Specify the security group ID to use for a newly created instance")
    parser.add_argument("--instance-type",
                        dest="instance_type",
                        required=False,
                        type=str,
                        help="Specify the instance type to use. "
                             f"Default is {DEFAULT_INSTANCE_TYPE}")
    parser.add_argument("--instance-name",
                        dest="instance_name",
                        required=False,
                        default=DEFAULT_INSTANCE_NAME,
                        type=str,
                        help="Specify the instance name. "
                             f"Default is {DEFAULT_INSTANCE_NAME}")
    options = parser.parse_args()
    if options.start and not options.security_group_id:
        parser.error('The --security-group-id arg cannot be blank when requesting to start a new instance. '
                     'Use --help for more info.')
    return options


class InstanceManager:
    def __init__(self):
        self.ec2 = boto3.resource('ec2')
        self.client = boto3.client('ec2')

    ## SSH KEY PAIRS
    ### GETTING KEY PAIRS
    def get_key_pairs(self):
        key_pairs = []
        response = self.client.describe_key_pairs()
        if response and 'KeyPairs' in response:
            for key_pair in response['KeyPairs']:
                key_pairs.append(key_pair)
        return key_pairs

    def print_key_pairs(self):
        key_pairs = self.get_key_pairs()
        if key_pairs:
            print('The SSH key pairs are:')
            print('Key-Pair-Name      Key-Pair-Id')
            for kp in key_pairs:
                key_pair_name = kp['KeyName']
                key_pair_id = kp['KeyPairId']
                print(f"{key_pair_name} {key_pair_id}")
        else:
            print('There are no SSH key pairs')

    ### CREATING A KEY PAIR
    def create_key_pair(self, key_name: str):
        print(f"Creating a new SSH key pair: {key_name}")
        response = self.client.create_key_pair(KeyName=key_name)
        if response and 'KeyMaterial' in response:
            private_key = response['KeyMaterial']
            file_name = f"{key_name}.pem"

            print(f'Saving the private key to {file_name}')
            with open(file_name, 'w') as f:
                f.write(private_key)
            # 0x400 -r--------
            os.chmod(file_name, 0o400)

    ### DELETE A KEY PAIR
    def delete_key_pair(self, key_name: str):
        print(f"Deleting the SSH key pair: {key_name}")
        self.client.delete_key_pair(KeyName=key_name)

        file_name = f"{key_name}.pem"
        if os.path.exists(file_name):
            os.chmod(file_name, 0o600)
            os.remove(file_name)

    ## SECURITY GROUPS
    ### GET SECURITY GROUPS
    def get_all_security_groups(self):
        security_groups = []
        response = self.client.describe_security_groups()
        if response and 'SecurityGroups' in response:
            for sg in response['SecurityGroups']:
                security_groups.append(sg)
        return security_groups

    def print_security_groups(self):
        def security_rule_to_string(rule: dict):
            if rule['IpProtocol'] == '-1':
                return f"{';'.join([ip['CidrIp'] for ip in rule['IpRanges']])} -> All Traffic"
            else:
                return f"{';'.join([ip['CidrIp'] for ip in rule['IpRanges']])} " \
                       f"-> {rule['FromPort']}/{rule['IpProtocol']}"

        security_groups = self.get_all_security_groups()
        if security_groups:
            print('Security groups are:')
            print("Group-Id   Group-Description    Ingress Permissions    Egress Permissions")
            for sg in security_groups:
                group_id = sg['GroupId']
                description = sg['Description']
                ip_permissions = []
                for rule in sg['IpPermissions']:
                    ip_permissions.append(security_rule_to_string(rule))

                ip_permissions_egress = []
                for rule in sg['IpPermissionsEgress']:
                    ip_permissions_egress.append(security_rule_to_string(rule))

                print(f"{group_id} {description} {ip_permissions} {ip_permissions_egress}")
                # print(group_id)
                # print(ip_permissions)
                # print(ip_permissions_egress)
                # print('*' * 50)

    ### CREATE A NEW SECURITY GROUP
    def create_security_group(self):
        pass

    ## EC2 INSTANCES
    def poll_ssh_status(self, instance_id):
        instance = self.get_instance(instance_id)
        # try until connected
        cmd = f"""
        until nc -w 1 -z {instance.public_ip_address} 22; do
             sleep 5
        done
        """
        try:
            os.system(cmd)
        except InterruptedError as e:
            print(f'Polling session with {instance.public_ip_address} has been interrupted')

    ### LISTING RUNNING INSTANCES
    def get_running_instances(self):
        # create filter for instances in running state
        filters = [
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]

        # filter the instances based on filters() above
        instances = []
        for instance in self.ec2.instances.filter(Filters=filters):
            instances.append(instance)
        return instances

    def get_instance(self, instance_id: str):
        return self.ec2.Instance(instance_id)

    def print_running_instances(self):
        instances = self.get_running_instances()
        if instances:
            print('Running instances are:')
            print('Instance-ID                Public-IP     Key-Pair-Name     Image-Id         Instance-Name')
            for instance in instances:
                instance_id = instance.id
                key_pair_name = instance.key_pair.key_name
                public_ip_address = instance.public_ip_address
                image_id = instance.image_id
                name = ''
                for tag in instance.tags:
                    if 'Key' in tag and tag['Key'] == 'Name':
                        name = tag['Value']
                print(f"{instance_id} {public_ip_address} {key_pair_name} {image_id} {name}")
                print(f"Connecting command: ssh ubuntu@{instance.public_ip_address} -i {key_pair_name}.pem")
        else:
            print('There are no running instances')

    ### TERMINATING INSTANCES
    def terminate_instance(self, instance_id: str):
        print(f'Terminating {instance_id}')
        self.client.terminate_instances(InstanceIds=[
            instance_id
        ])

    def terminate_all_running_instances(self):
        print('Terminating all running instances')
        for instance in self.get_running_instances():
            self.terminate_instance(instance.id)

    ### STARTING INSTANCES
    def run_instance(self,
                     image_id: str,
                     key_pair_name: str,
                     security_group_id: str,
                     instance_type: str = 't2.micro',
                     instance_name: str = 'My-Awesome-Instance'):
        print(f'Starting a new instance: '
              f'{image_id} {key_pair_name} {security_group_id} {instance_type} {instance_name}')
        response = self.client.run_instances(InstanceType=instance_type,
                                             ImageId=image_id,
                                             KeyName=key_pair_name,
                                             SecurityGroupIds=[security_group_id],
                                             TagSpecifications=[
                                                 {
                                                     'ResourceType': 'instance',
                                                     'Tags': [
                                                         {
                                                             'Key': 'Name',
                                                             'Value': instance_name
                                                         },
                                                     ]
                                                 },
                                             ],
                                             # The maximum number of instances to launch.
                                             # If you specify more instances than Amazon EC2 can launch
                                             # in the target Availability Zone,
                                             # Amazon EC2 launches the largest possible number of instances above MinCount.
                                             MaxCount=1,
                                             MinCount=1
                                             )
        return response['Instances']


if __name__ == '__main__':
    options = get_arguments()

    key_pair_name = options.key_pair_name
    image_id = options.image_id
    security_group_id = options.security_group_id
    instance_type = options.instance_type
    instance_name = options.instance_name

    server_manager = InstanceManager()

    if options.terminate_all:
        server_manager.terminate_all_running_instances()

    if options.status:
        server_manager.print_running_instances()
        print('*' * 50)
        server_manager.print_key_pairs()
        print('*' * 50)
        server_manager.print_security_groups()
    elif options.start:
        if options.force_recreate_key:
            server_manager.delete_key_pair(key_name=key_pair_name)
        try:
            server_manager.create_key_pair(key_name=key_pair_name)
        except Exception as e:
            if 'InvalidKeyPair.Duplicate' in f"{e}":
                print(f"The SSH key pair '{key_pair_name}' already exists")
            else:
                print(f"{type(e)} {e}")
                exit(1)

        new_instance = server_manager.run_instance(image_id=image_id,
                                                   key_pair_name=key_pair_name,
                                                   security_group_id=security_group_id,
                                                   instance_name=instance_name)[0]

        if new_instance:
            print('The instance has been created')
            print('Waiting for the server boot...')
            instance = server_manager.get_instance(new_instance['InstanceId'])
            instance.wait_until_running()
            print('The server is up and running')
            server_manager.print_running_instances()
            print('Waiting until the SSH service is up...')
            server_manager.poll_ssh_status(instance.id)
