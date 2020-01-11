#!/usr/bin/env python3
from argparse import ArgumentParser
import os


ACCESS_MODES = {
    "f": os.F_OK,
    "r": os.R_OK,
    "w": os.W_OK,
    "x": os.X_OK,
}


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-p', '--path', required=True, help="A directory to parse. Will walk through subdirectories recursively")
    parser.add_argument('-m', '--mask', required=True, help="A string of access modes to check. Any combination of: f, r, w, x")

    options = parser.parse_args()

    return options.path, options.mask


def check_access_mode(walking_root, mask_string):
    try:
        mask = set(ACCESS_MODES[m.lower()] for m in mask_string)
        for dirpath, dirnames, filenames in os.walk(walking_root):
            for dirname in dirnames:
                for filename in filenames:
                    path = os.path.join(dirpath, dirname, filename)
                    has_access = all(os.access(path, mode) for mode in mask)
                    if has_access:
                        print("{} has {} access".format(path, mask_string))
    except KeyError:
        print("{} is not one of the possible file access mods (f, r, w, x)".format(mask_string))
    except Exception as e:
        print(type(e), e)


if __name__ == "__main__":
    path, mask = parse_args()
    check_access_mode(path, mask)

