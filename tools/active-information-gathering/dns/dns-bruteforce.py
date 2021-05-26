#!/usr/bin/env python3
import socket
from os import linesep
from threading import Thread

DEFAULT_THREADS_LIMIT = 10
socket.setdefaulttimeout(5)


def get_arguments():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--wordlist',
                        dest='wordlist',
                        required=True,
                        type=str,
                        help='Specify a wordlist file to use while bruteforcing the host')
    parser.add_argument('--target',
                        dest='target',
                        required=True,
                        type=str,
                        help='Specify a target for the bruteforcing with a wildcard "*" symbol as the injection marker.')
    parser.add_argument('--threads',
                        dest='threads',
                        default=DEFAULT_THREADS_LIMIT,
                        required=False,
                        type=int,
                        help='Specify the threads limit for the dns bruteforcing. '
                             f'Default is {DEFAULT_THREADS_LIMIT}')
    options = parser.parse_args()
    if '*' not in options.target:
        parser.error('Your target doesn\'t have an injection marker - "*". Use --help for more info')
    return options


def do_dns_lookup(domain):
    global counter
    global wordlist_size
    print(f"[{counter}/{wordlist_size}] Searching...", end='\r', flush=True)
    try:
        ip = socket.gethostbyname(domain)
        print(f'{linesep}{domain} - {ip}')
    except:
        pass
    counter += 1


options = get_arguments()
target = options.target
threads_limit = options.threads
with open(options.wordlist, 'r', errors='ignore') as f:
    wordlist = [line.strip() for line in f.readlines()]

dns_threads = []
counter = 0
wordlist_size = len(wordlist)
for domain in wordlist:
    while len(dns_threads) >= threads_limit:
        for thread in dns_threads.copy():
            if not thread.is_alive():
                dns_threads.remove(thread)

    dns_thread = Thread(target=do_dns_lookup, args=(target.replace('*', domain),))
    dns_threads.append(dns_thread)
    dns_thread.start()

while any(thread.is_alive() for thread in dns_threads):
    pass
