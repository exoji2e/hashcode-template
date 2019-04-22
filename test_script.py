import argparse
import random
from score import parse
import sys

# ns is the namespace. 
# If needed write a simple parser which returns ns.
# If simple parser should be used run the program with extra argument ('sp')
def test(ns):
    # TODO: Write the tests to print given ns.
    pass

def simple_parse(inp):
    pass

if __name__=='__main__':
    args = sys.argv
    with open(args[-1]) as f:
        inp = f.read()
    if len(sys.argv) > 2:
        ns = simple_parse(inp)
    else: 
        ns = parse(inp)

    test(ns)
