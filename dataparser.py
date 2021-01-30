import argparse
import json
from collections import *
from pathlib import Path

def ni(itr):
    return int(next(itr))

# parses the next string of itr as a list of integers
def nl(itr):
    return [int(v) for v in next(itr).split()]


def parse(inp):
    itr = (line for line in inp.split('\n'))
    ns = argparse.Namespace()
    # TODO: fill ns

    return ns

class FlexibleEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, argparse.Namespace):
            return vars(obj)
        return json.JSONEncoder.default(self, obj)

def parse2json(inp):
    ns = parse(inp)
    return json.dumps(ns, cls=FlexibleEncoder)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('inp', nargs='?')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    if args.inp:
        file_list = [args.inp]
    else:
        file_list = Path('in').glob('*.in')

    for inp in file_list:
        data = parse2json(inp.read_text())
        with inp.with_suffix('.json').open('w') as f:
            f.write(data)
