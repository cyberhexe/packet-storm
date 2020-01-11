#!/usr/bin/env python3
import socket
from argparse import ArgumentParser

import termcolor

DEFAULT_FUZZING_COUNT = 30


def get_arguments():
    parser = ArgumentParser()
    parser.add_argument('-i', '--ip',
                        dest='ip',
                        required=True,
                        help='IP address to fuzz')
    parser.add_argument('-p', '--port',
                        dest='port',
                        required=True,
                        help='TCP port to fuzz')
    parser.add_argument('-c', '--count',
                        dest='count',
                        default=DEFAULT_FUZZING_COUNT,
                        required=False,
                        help='A number of attempts to fuzz the service. '
                             'Default is ' + str(DEFAULT_FUZZING_COUNT))
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Be verbose, print the service output')
    options = parser.parse_args()
    return options


class Fuzzer:
    def __init__(self, ip, port, counts, verbose=False):
        self.ip = ip
        self.port = port
        self.verbose = verbose
        self.payload = ["A"]
        self.connection = None
        counter = 100
        while len(self.payload) <= counts:
            self.payload.append("A" * counter)
            counter += 200

        self.response_history = []

    def log(self, message, color=None):
        if not color:
            message = message
        else:
            message = termcolor.colored(message, color)
        print("{ip}:{port} - {message}".format(ip=self.ip,
                                               port=self.port,
                                               message=message))

    def open_connection(self, ip: str, port: int):
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((ip, port))
        except Exception as e:
            self.log(e)
            raise Exception("Connection cannot be established")

    def close_connection(self):
        try:
            self.connection.close()
        except Exception as e:
            self.log(e)
            exit()

    def send(self, message: str, enc='utf-8'):
        try:
            self.connection.send(bytes(message, encoding=enc))
        except Exception as e:
            self.log(e)
            return

    def receive(self):
        try:
            resp = self.connection.recv(1024)
            if resp and len(resp) > 0:
                result = str(resp)[2:-5]
                if self.verbose:
                    if result not in self.response_history:
                        self.log(result, color='red')
                        self.response_history.append(result)
                    else:
                        self.log(result, color='green')
                return result
        except Exception as e:
            self.log(e)
            return

    def fuzz(self):
        for string in self.payload:
            self.open_connection(self.ip, self.port)
            self.log('Fuzzing with {len} bytes'.format(len=str(len(string))))
            try:
                self.receive()
                self.send('{payload}\r\n'.format(payload=string))
                self.connection.close()
            except Exception as e:
                self.log(e)
                exit()
        self.log('Fuzzing finished')


options = get_arguments()
fuzzer = Fuzzer(options.ip, int(options.port), int(options.count), options.verbose)
try:
    fuzzer.fuzz()
except KeyboardInterrupt:
    print('\n\nInterrupted')
    exit(0)
