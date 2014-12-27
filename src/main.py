#!/bin/env python3

__author__ = "Peter Leontev"

import sys
sys.path.append('ugene_elements')

import converter
from argparse import ArgumentParser


def create_parser():
    parser = ArgumentParser(description="Convert workflow scheme")
    parser.add_argument("-scheme", help = ".uwl workflow scheme filename")

    return parser

def show_usage():
    print('Please, use -scheme option to set UGENE workflow scheme, e.g. "-scheme test.uwl"')


def get_args(parser):
    args = parser.parse_args()

    return args.scheme


def main():
    parser_obj = create_parser()
    arg        = get_args(parser_obj)

    if arg == None:
        show_usage()
        return 0

    scheme_filename = arg

    converter_obj = converter.Converter(scheme_filename)
    code = converter_obj.convert()

    four_spaces = " " * 4
    result = ""

    indentation = 0

    for line in code:
        if line != "indentation end":
            result += four_spaces * indentation + line + "\n"

            if line.startswith("for") or line.startswith("if") or line.startswith("with"):
                indentation += 1
        else:
            indentation -= 1



    with open(scheme_filename[:-3] + "py", "w") as outp:
        outp.write(result)


if __name__ == "__main__":
    main()
