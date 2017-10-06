#!/usr/bin/env  python

import argparse
import sys
import os
import csv

__author__ = "Andrew Mulheirn"
__copyright__ = "Copyright 2016, Axians Networks Limited"
__version__ = "0.1"
__maintainer__ = "Andrew Mulheirn"
__email__ = "andrew.mulheirn@axians.co.uk"
__status__ = "Test"

parser = argparse.ArgumentParser(description='''
Takes one or more CSV files, each containing device parameters, and
turns them into YAML for use by Ansible/Jinja2 config generation process.''',
                                 epilog='''
This software is provided with no warranty. Based on work by Andrew Mulheirn.
https://github.com/amulheirn/confgen2''')

parser.add_argument('-o', nargs='?', type=argparse.FileType('wb', 0),
                    default=sys.stdout, metavar='outFile',
                    help='YAML file to write to')

parser.add_argument('-i', nargs='*', type=argparse.FileType('rb', 0),
                    default=sys.stdin, metavar='inFile',
                    help='CSV file(s) to read from')

parser.add_argument('-debug', action='store_true', help='Enable Debug Mode')

args = parser.parse_args()

debug = args.debug
out_file = args.o

if debug:
    print >> sys.stderr, args

out_file.write("---\n")

for in_file in args.i:
    list_name = "stdin"
    try:
        list_name = os.path.splitext(os.path.basename(in_file.name))[0]
    except AttributeError as error:
        print >> sys.stderr, "Dictionary will named %s, this mode is flaky." % (list_name)

    list_name = list_name.replace("-", "_")

    if debug:
        print >> sys.stderr, "%s -> %s\n" % (list_name, out_file.name)
    reader = csv.DictReader(in_file, dialect='excel')
    out_file.write("%s:\n" % (list_name))
    try:
        for row in reader:
            out_file.write("  - { ")
            for item, value in row.iteritems():
                out_file.write("%s: %s, " % (item, value))
            out_file.write("}\n")
    except csv.Error as error:
        sys.exit("outfile %s, infile %s, line %d:, %s" % (out_file, in_file,
                                                       reader.line_num, error))

