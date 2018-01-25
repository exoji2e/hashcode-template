from score import score
import random
from random import randint as ri
import logging as log
import argparse


# Runs scoring function and checks if score is improved.
def process(out, seed):
    sc = score(inp, out)

    try:
        with open(args.testcase + '.max', 'r') as f:
            bsc = int(f.readline())
    except:
        bsc = 0

    if sc > bsc:
        log.critical('New best score {} for testcase {}'.format(sc, args.testcase))
        fname = '_'.join([args.testcase, str(sc), seed]) + '.ans'

        with open(args.testcase + '.max', 'w') as f:
            f.write(str(sc))

        with open('ans/' + fname, 'w') as f:
            # Print to f
            f.write(str(out))
    else:
        log.warn('Score: {}'.format(sc))


def greedy(seed):
    # TODO: Solve the problem
    random.seed(seed)

    process(0, seed)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('testcase')
    parser.add_argument('-l', '--log', default='debug')
    parser.add_argument('-s', '--seed', default=None)
    parser.add_argument('-n', '--iterations', default=10)
    return parser.parse_args()


def init_log():
    loglvls = {'debug': log.DEBUG, 'info': log.INFO, 'warning': log.WARNING, 'error': log.ERROR, 'critical': log.CRITICAL}
    logfmt = '%(relativeCreated)6d %(message)s ' + args.testcase
    log.basicConfig(level=loglvls[args.log], format=logfmt)


if __name__ == '__main__':
    args = get_args()
    init_log()

    with open('in/' + args.testcase + '.in') as f:
        inp = f.read()
        # TODO: Proccess input data

    if args.seed:
        log.info('seed: {}'.format(args.seed))
        greedy(args.seed)
    else:
        for i in range(args.iterations):
            seed = ri(0, 10000)
            log.info('seed: {}, test#: {}'.format(seed, i))
            greedy(seed)
