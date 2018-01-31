import random
import argparse
import logging as log
from random import randint as ri
from util import mkdir


# Runs scoring function and checks if score is improved.
def process(out, seed):
    scoring = args.scoring.split(":")
    score_module = scoring[0]
    score_fun = "score"
    if len(scoring) > 1:
        score_fun = scoring[1]

    score = __import__(score_module, globals(), locals(), [], 0)
    sc = getattr(score, score_fun)(inp, out)

    try:
        with open(args.testcase + '.max', 'r') as f:
            bsc = int(f.readline())
    except IOError:
        bsc = 0

    fmt = 'Score: {:<20}'
    if sc > bsc:
        log.critical((fmt + " BEST").format(sc))

        with open(args.testcase + '.max', 'w') as f:
            f.write(str(sc))

        mkdir('ans')
        fname = '_'.join([args.testcase, str(sc), seed]) + '.ans'
        with open('ans/' + fname, 'w') as f:
            # Print to f
            f.write(str(out))
    else:
        log.warn(fmt.format(sc))


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
    parser.add_argument('--scoring', action='store', default="score:score")
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
