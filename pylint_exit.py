#!/usr/local/bin/python
from __future__ import print_function
import sys
from bitarray import bitarray
import argparse


# Package information
version = __version__ = "0.1.0rc1"
__title__ = "pylint_exit"
__summary__ = "Exit code handler for pylint command line utility."
__uri__ = "https://github.com/jongracecox/pylint-exit"


EXIT_CODES_LIST = [
    (1, 'fatal message issued', 1),
    (2, 'error message issued', 0),
    (4, 'warning message issued', 0),
    (8, 'refactor message issued', 0),
    (16, 'convention message issued', 0),
    (32, 'usage error', 1)
    ]


def decode(value):
    """
    Decode the return code value into a bit array.

    Args:
        value(int): Return code from pylint command line.

    Returns:
        list of raised exit codes.
    """
    return [x[1] for x in zip(bitarray(bin(value)[2:])[::-1], EXIT_CODES_LIST) if x[0]]


def get_messages(value):
    """Return a list of raised messages for a given pylint return code"""
    return [x[1] for x in decode(value)]


def get_exit_code(value):
    exit_codes = [x[2] for x in decode(value)]
    if not exit_codes:
        return 0
    else:
        return max(exit_codes)


def show_workings(value):
    print("%s (%s) = %s" %
          (value, bin(value)[2:], [x[1][1] for x in zip(bitarray(bin(value)[2:])[::-1], EXIT_CODES_LIST) if x[0]]))


def handle_exit_code(value):
    messages = get_messages(value)
    exit_code = get_exit_code(value)

    if messages:
        print("The following messages were raised:")
        print('')

    for m in messages:
        print("  - %s" % m)

    if messages:
        print('')

    if exit_code:
        print("Fatal messages detected.  Failing...")
    else:
        print("No fatal messages detected.  Exiting gracefully...")

    return exit_code


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('pylint_exit_code', metavar='PYLINTRC', type=int,
                    help='pylint return code')
    return parser.parse_args()


def main():
    args = parse_args()
    exit_code = handle_exit_code(args.pylint_exit_code)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
