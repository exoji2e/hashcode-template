#!/usr/bin/env pypy2
import argparse
import random


def parse(inp):
    # TODO: implement
    itr = (map(int, li.split()) for li in inp.split('\n'))
    r, c = next(itr)

    return argparse.Namespace(r=r, c=c)


def solve(seed, inp, log):
    # TODO: Solve the problem
    random.seed(seed)
    ns = parse(inp)

    return '0'
