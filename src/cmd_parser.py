from argparse import ArgumentParser

def create():
    parser = ArgumentParser(description="Convert workflow scheme")
    parser.add_argument("-scheme", help = ".uwl workflow scheme filename")
    
    return parser

def usage():
    print('Please, use -s option to set UGENE workflow scheme, e.g. "-s test.uwl"')
    

def get_args(parser):
    args = parser.parse_args()
    
    return args.scheme
    