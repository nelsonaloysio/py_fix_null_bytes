#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Remove null byte characters from file.

usage: fix_null_bytes.py [-h] [-o OUTPUT] input

positional arguments:
  input                 input file name

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output file name
'''

from argparse import ArgumentParser
from os.path import basename, splitext
from sys import argv

def fix_null_bytes(input_name, output_name=None):
    '''
    Python CSV streaming code is written using C based I/O,
    causing the null byte character to short out the reading
    of data in an abrupt and non-recoverable manner.

    To get around this we pre-process the stream by wrapping
    the file with a function that removes null byte characters.

    Note that Bash offers a simple alternative for this:
    $ cat input_file.ext | tr -d '\0' > output_file
    '''
    print('Removing null bytes...')

    if not output_name:
        name, ext = splitext(basename(input_name))
        output_name = name + '_FIXED' + ext

    with open(input_name, 'rb') as input_file:
        with open(output_name, 'wb') as output_file:
            for line in input_file:
                output_file.write(line.replace(b'\x00', bytes('', 'utf8')))

if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument('input', action='store', help='input file name')
    parser.add_argument('-o', '--output', action='store', help='output file name')

    args = parser.parse_args()

    fix_null_bytes(args.input,
                   args.output)