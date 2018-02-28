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


def show(out):
    # TODO: Print the solution here
    print(out)


def score(inp, out):
    # TODO: implement

    if __name__ == '__main__' and args.s:
        show(out)

    return 0


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-inp', default='')
    parser.add_argument('-ans', default='')
    parser.add_argument('-s', action='store_true', help="show")
    parser.add_argument('-t', action='store', help="will look for in/testcase.in and submission/testcase.ans")
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    if args.t:
        args.inp = 'in/' + args.t + '.in'
        args.ans = 'submission/' + args.t + '.ans'

    with open(args.inp, 'r') as f:
        inp = f.read()

    with open(args.ans, 'r') as f:
        ans = f.read()

    print(score(inp, ans))
