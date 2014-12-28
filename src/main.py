#!/bin/env python3

__author__ = "Peter Leontev"

import sys
sys.path.append('ugene_elements')

import converter
from argparse import ArgumentParser


def show_usage():
    print('Please, use -scheme option to set UGENE workflow scheme, e.g. "-scheme test.uwl"')


def main():
    parser = ArgumentParser(description="Convert workflow scheme")
    parser.add_argument("-scheme", help=".uwl workflow scheme filename")

    scheme_filename = parser.parse_args().scheme

    if scheme_filename == None:
        show_usage()
        return 0

    converter_obj = converter.Converter(scheme_filename)
    code = converter_obj.convert()

    with open(scheme_filename[:-3] + "py", "w") as outp:
        outp.write(code)


if __name__ == "__main__":
    main()
