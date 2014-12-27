#!/bin/env python3

__author__ = "Peter Leontev"

import cmd_parser
import converter

def main():
    parser_obj = cmd_parser.create()
    arg       = cmd_parser.get_args(parser_obj)    
    
    if arg == None:
        cmd_parser.usage()
        return 0
    
    scheme_filename = arg
    
    converter_obj = converter.Converter(scheme_filename)
    code = converter_obj.convert()
          
    with open(scheme_filename[:-3] + "py", "w") as outp: 
        indentation = 0         
            
        for line in code:
            if line != "indentation end":
                outp.write("    " * indentation + line + "\n")
                
                if line.startswith("for") or line.startswith("if") or line.startswith("with"):
                    indentation += 1  
            else:
                indentation -= 1


if __name__ == "__main__":
    main()     
