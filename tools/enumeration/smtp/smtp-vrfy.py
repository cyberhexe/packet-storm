#!/usr/bin/env python3

import smtplib
from argparse import ArgumentParser


def get_arguments():
    parser = ArgumentParser()
    parser.add_argument('-i', '--ip', dest='ip',
                        help='IP address with a SMTP service')
    parser.add_argument('-iL', '--ip-list', dest='ip_list',
                        help='Provide a new-line separated list of the IP addresses to enumerate user(s)')
    parser.add_argument('-u', '--user', dest='user',
                        help='A single username to check')
    parser.add_argument('-w', '--wordlist', dest='wordlist',
                        help='A wordlist with users to enumerate')
    parser.add_argument('-p', '--port',
                        help='SMTP port. Default is 25.', default=25)
    options = parser.parse_args()
    if not options.ip and not options.ip_list:
        parser.error('IP address cannot be blank')
    if not options.wordlist and not options.user:
        parser.error('Missing users list or username')
    return options


class SMTPClient:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def init(self):
        self.log(f'Connecting to smtp://{self.ip}:{self.port}')
        self.client = smtplib.SMTP(host=self.ip, port=self.port, timeout=2)
        self.log(f'Connected')

    def verify(self, username):
        print(f'localhost - VRFY {username}')
        self.client.ehlo_or_helo_if_needed()
        resp = self.client.verify(username)
        if resp:
            code = resp[0]
            message = str(resp[1])[2:-1]
            self.log(f'{code} {message}')
        else:
            self.log('No response')

    def log(self, message):
        print(f'smtp://{self.ip}:{self.port} - {message}')


try:
    if __name__ == '__main__':
        options = get_arguments()


        def do_enumerate(ip, port):
            try:
                smtp_client = SMTPClient(ip, port)
                smtp_client.init()
                if options.user:
                    smtp_client.verify(options.user)
                elif options.wordlist:
                    for user in [user.replace('\n', '') for user in open(options.wordlist).readlines()]:
                        smtp_client.verify(user)
            except Exception as e:
                smtp_client.log(e)


        if options.ip and not options.ip_list:
            do_enumerate(options.ip, options.port)
        elif options.ip_list:
            for address in [ip.replace('\n', '') for ip in open(options.ip_list, 'r').readlines()]:
                if ':' not in address:
                    ip = address
                    port = 25
                    do_enumerate(ip, port)
                else:
                    ip = address.split(':')[0]
                    port = int(address.split(':')[1])
                    do_enumerate(ip, port)
except KeyboardInterrupt:
    print('\n\nInterrupted')
    exit()
