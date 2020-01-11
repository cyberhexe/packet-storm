#!/usr/bin/env python3
import logging
import random
import string
from argparse import ArgumentParser
from datetime import datetime
from threading import Thread
from time import sleep

THREAD_POOL_EXHAUSTED_LIMIT = 10
SLEEP_TIMER_IN_SECONDS = 10

logging.basicConfig(format='[%(asctime)s %(levelname)s] - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level='INFO')


def get_arguments():
    parser = ArgumentParser(
        description='Use this template to wrap your code in a specified number of parallel threads')
    parser.add_argument('--threads',
                        dest='threads',
                        default=THREAD_POOL_EXHAUSTED_LIMIT,
                        required=False,
                        help='A number of threads to use in parallel. Default is ' + str(
                            THREAD_POOL_EXHAUSTED_LIMIT) + ".")
    options = parser.parse_args()
    return options


class JobThread:
    def __init__(self, target_function, target_function_args=None):
        assert target_function, "Function to run within the thread must be given"
        random_uid = ''.join([random.choice(string.ascii_letters
                                            + string.digits) for n in range(15)])
        self.uid = "THREAD-{uid}".format(uid=random_uid)
        self.thread = Thread(target=target_function, args=target_function_args)

    def start(self):
        logging.info('[{thread_uid}] Starting the thread...'.format(thread_uid=self.uid))
        self.thread.start()

    def isAlive(self):
        return self.thread.isAlive()


def create_parallel_jobs(jobs_list,
                         thread_limit=THREAD_POOL_EXHAUSTED_LIMIT,
                         sleep_timer_in_seconds=SLEEP_TIMER_IN_SECONDS):
    threads = []
    for something in jobs_list:
        while len(threads) >= thread_limit:
            logging.warning('Thread pool is exhausted, will sleep for {sleep} seconds and continue...'.format(
                sleep=sleep_timer_in_seconds))
            sleep(sleep_timer_in_seconds)
            for thread in threads.copy():
                if not thread.isAlive():
                    threads.remove(thread)
        try:
            thread = JobThread(target_function=job, target_function_args=(something,))
            thread.start()
            threads.append(thread)
        except Exception as e:
            logging.error('{exception}'.format(exception=e))

    while any(thread.isAlive() for thread in threads):
        logging.warning('\nNot all threads have finished yet, putting the main thread to sleep for {sleep} seconds'
                        .format(datetime=str(datetime.now()), sleep=sleep_timer_in_seconds))
        sleep(sleep_timer_in_seconds)
    logging.info('All threads have been finished')


def job(args):
    # print here your code
    print('Doing something important in parallel...')


options = get_arguments()
create_parallel_jobs([i for i in range(0, 100)], int(options.threads))
