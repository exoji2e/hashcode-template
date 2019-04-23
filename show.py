import argparse
import random
from score import parse, nl, ni
import sys

# ns is the namespace. 
# If needed write a simple parser which returns ns.
# If simple parser should be used run the program with extra argument ('sp')
def test(inp):
    print(inp)
    # TODO: Write the tests to print given inp.
    # Use parse from score, or write your own (simple_parse)

def simple_parse(inp):
    itr = (line for line in inp.split('\n'))
    ns = argparse.Namespace()
    return ns

if __name__=='__main__':
    args = sys.argv
    inp = open(args[-1]).read()

    test(inp)
