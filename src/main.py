#!/bin/env python3

__author__ = "Peter Leontev"

import cmd_parser
import converter

def main():
    parser_obj = cmd_parser.create()
    args       = cmd_parser.get_args(parser_obj)    
    
    if args == None:
        cmd_parser.usage()
        return 0 
    
    scheme_filename = parser_obj.scheme 
    
    converter_obj = converter.Converter(scheme_filename)
    result        = converter_obj.convert()
    
    with open(scheme_filename[:-3], "w" ) as outp:
        outp.write(result)
        
    
    return 0


if __name__ == "__main__":
    main()     
