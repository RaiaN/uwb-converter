from argparse import ArgumentParser

def create():
    parser = ArgumentParser(description="Convert workflow scheme")
    parser.add_argument("-scheme", help = ".uwl workflow scheme filename")
    
    return parser

def usage():
    print('Please, use -scheme option to set UGENE workflow scheme, e.g. "-scheme test.uwl"')
    

def get_args(parser):
    args = parser.parse_args()
    
    return args.scheme
    