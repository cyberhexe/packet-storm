#!/usr/bin/env python3
import subprocess
from argparse import ArgumentParser


def get_arguments():
    parser = ArgumentParser()
    parser.add_argument('-n', '--network', dest='network',
                        help='A network range to perform ping scan')
    options = parser.parse_args()
    if not options.network:
        parser.error('A network range /24 must be provided')
    if '/24' not in options.network:
        parser.error('Invalid network range, only /24 is supported')
    return options


options = get_arguments()

network_range = options.network
for i in range(0, 255):
    chunks = network_range.split('/24')[0].split('.')
    address = f'{chunks[0]}.{chunks[1]}.{chunks[2]}.{i}'
    try:
        command = f'ping -c 1 {address} |grep "bytes from" |cut -d ":" -f1 |cut -d " " -f4 &'
        # command = f'ping -c 1 {address}'
        result = subprocess.call(command, shell=True)
    except Exception as e:
        continue
