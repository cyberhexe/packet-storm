#!/usr/bin/env python3
from scapy.all import ARP, Ether, srp
from datetime import datetime

# pip3 install scapy

DEFAULT_TIMEOUT_IN_SECONDS = 5


def get_arguments():
    from argparse import ArgumentParser
    parser = ArgumentParser(description="ARP Scanner Script")
    parser.add_argument('-i',
                        '--interface',
                        dest='interface',
                        required=True,
                        type=str,
                        help='Specify the network interface to use')
    parser.add_argument('--target',
                        dest='target',
                        required=True,
                        type=str,
                        help='Specify the target IP address or the target subnet to scan')
    parser.add_argument('--timeout',
                        dest='timeout',
                        required=False,
                        default=DEFAULT_TIMEOUT_IN_SECONDS,
                        type=int,
                        help='Specify the timeout in seconds.'
                             f'Default is {DEFAULT_TIMEOUT_IN_SECONDS}.')
    parser.add_argument('-v',
                        '--verbose',
                        dest='verbose',
                        required=False,
                        action='store_true',
                        help='Be verbose - print additional information. '
                             'Disabled by default.')
    options = parser.parse_args()
    return options


def do_arp_scan(target: str,
                iface: str,
                timeout: int = DEFAULT_TIMEOUT_IN_SECONDS,
                verbose: bool = False):
    # create ARP packet
    arp = ARP(pdst=target)

    # create the Ether broadcast packet
    # ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")

    # stack them
    packet = ether / arp

    if verbose:
        print(f"Starting an ARP scan at {datetime.now()}")
    result = srp(packet, iface=iface, timeout=timeout, verbose=verbose)[0]

    # a list of clients, we will fill this in the upcoming loop
    clients = []

    for sent, received in result:
        # for each response, append ip and mac address to `clients` list
        clients.append({'ip': received.psrc, 'mac': received.hwsrc})

    if verbose:
        print(f"The ARP scan finished at {datetime.now()}")
    print("Available devices in the network:")
    for client in clients:
        print("{:16}    {}".format(client['ip'], client['mac']))


def main():
    options = get_arguments()
    target = options.target
    iface = options.interface
    timeout = options.timeout
    verbose = options.verbose

    do_arp_scan(target=target,
                iface=iface,
                timeout=timeout,
                verbose=verbose)


if __name__ == '__main__':
    main()
