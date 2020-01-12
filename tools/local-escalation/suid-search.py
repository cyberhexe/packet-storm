#!/usr/bin/env python3
import os
import stat
import sys
from pwd import getpwuid

def find_owner(filename):
    return getpwuid(os.stat(filename).st_uid).pw_name


def check_access_mode(walking_root):
    platform = sys.platform
    try:
        for dirpath, dirnames, filenames in os.walk(walking_root):
            if dirnames:
                for dirname in dirnames:
                    iter_files_in_directory(dirname, dirpath, filenames)
            else:
                iter_files_in_directory(dirpath, None, filenames)
    except:
        pass


def iter_files_in_directory(dirpath, dirname, filenames, platform='linux'):
    for filename in filenames:
        if dirname:
            path = os.path.join(dirpath, dirname, filename)
        else:
            path = os.path.join(dirpath, filename)
        if not os.path.exists(path):
            continue
        if 'linux' in platform:
            # check the file for the SUID/SGID bit
            # https://stackoverflow.com/a/2163835
            # check the file's ownership
            # https://stackoverflow.com/a/1830635

            appstat = os.stat(path)
            if appstat.st_mode & stat.S_ISUID:
                print('ROOT SUID ' + path)
                if find_owner(path) == 'root':
                    f = open('suid.txt', 'a')
                    f.write(path.split('/')[-1])
                    f.write(os.linesep)
                    f.close()


if __name__ == "__main__":
    path = sys.argv[1]
    check_access_mode(path)
