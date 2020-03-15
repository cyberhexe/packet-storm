#!/usr/bin/env python3
from socket import gethostbyname

from requests_html import HTMLSession


def get_arguments():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('--hostname',
                        dest='hostname',
                        required=False,
                        help='Specify a hostname of the target to obtain the IP address '
                             'and get the neighbours host-names.')
    parser.add_argument('--ip',
                        dest='ip',
                        required=False,
                        help='Specify an IP address to find which host-names are belong to it.')
    options = parser.parse_args()

    return options


def get_hostnames(ip):
    try:
        with HTMLSession() as session:
            resp = session.get(f'https://www.bing.com/search?q=ip%3A{ip}')
            return handle_response(resp)
    except Exception as e:
        print(e)


def handle_response(resp):
    hostnames = set()
    for link in resp.html.absolute_links:
        if 'microsoft' in link or 'bing' in link:
            continue
        else:
            hostnames.add(link)
    return hostnames


options = get_arguments()

links = set()
if options.ip:
    links = get_hostnames(options.ip)
elif options.hostname:
    links = get_hostnames(gethostbyname(options.hostname))

if links:
    print(f'Found {len(links)} links')
    for host in links:
        print(host)
