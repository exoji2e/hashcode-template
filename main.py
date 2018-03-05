#!/usr/bin/env pypy
import argparse
import logging as log
from random import randint as ri
from util import mkdir
from os import remove
from ConfigParser import ConfigParser


# Runs scoring function and checks if score is improved.
def process(inp, out, seed, sc_fun):

    # Remember to edit if minimization-problem.
    try:
        with open(args.testcase + '.max', 'r') as f:
            bsc = int(f.readline())
    except IOError:
        bsc = 0

    try:
        sc = sc_fun(inp, out)
    except Exception as e:
        if not args.ignore:
            raise
        log.error(str(e))
        sc = 0

    fmt = 'score: {:<20}'
    # write new output file.
    if sc > bsc:
        log.critical((fmt + " BEST").format(sc))

        with open(args.testcase + '.max', 'w') as f:
            f.write(str(sc))

        mkdir('ans')
        fname = '{}_{}_{}.ans'.format(args.testcase, sc, seed)
        fpath = 'ans/' + fname
        with open(fpath, 'w') as f:
            f.write(str(out))
        mkdir('submission')
        latest = "submission/{}.ans".format(args.testcase)
        try:
            remove(latest)
        except OSError:
            pass
        with open(latest, 'w') as f:
            f.write(str(out))
    else:
        log.warn(fmt.format(sc))


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('testcase')
    parser.add_argument('-l', '--log', default='debug', help="set the log level")
    parser.add_argument('-s', '--seed', default=None, help="provide a seed for the rng")
    parser.add_argument('-n', '--iterations', type=int, default=1, help="number of iterations to run the solver")
    parser.add_argument('-i', '--ignore', action='store_true', help="do not fail on scoring errors")
    parser.add_argument('-c', '--config', action='store', default='', help="config file")
    parser.add_argument('--score', action='store', default='', help="set scoring config, format: key1=value1,key2=value2")
    parser.add_argument('--solve', action='store', default='', help="set solve config, format: key1=value1,key2=value2")
    return parser.parse_args()


def init_log():
    loglvls = {'debug': log.DEBUG, 'info': log.INFO, 'warning': log.WARNING, 'error': log.ERROR, 'critical': log.CRITICAL}
    logfmt = '%(relativeCreated)6d {} %(filename)12s:%(lineno)-3d %(message)s'.format(args.testcase)
    log.basicConfig(level=loglvls[args.log], format=logfmt)


if __name__ == '__main__':
    args = get_args()
    args.testcase = args.testcase.replace('in/', '').replace('.in', '').replace('.max', '')
    init_log()
    config = ConfigParser()
    config.read(['main.cfg', args.config])

    for k, v in (e.split('=') for e in args.score.split(',') if e):
        config.set('score', k, v)

    for k, v in (e.split('=') for e in args.solve.split(',') if e):
        config.set('solve', k, v)

    score_module = config.get('score', 'module')
    solve_module = config.get('solve', 'module')
    score_fun_name = config.get('solve', 'function')
    solve_fun_name = config.get('score', 'function')

    sol = __import__(solve_module, globals(), locals(), [], 0)
    sc = __import__(score_module, globals(), locals(), [], 0)
    sc_fn = getattr(sc, score_fun_name)
    sol_fn = getattr(sol, solve_fun_name)

    with open('in/' + args.testcase + '.in') as f:
        inp = f.read()

    def run(seed):
        ans = sol_fn(seed, inp, log)
        process(inp, ans, seed, sc_fn)

    if args.seed:
        log.info('seed: {}'.format(args.seed))
        run(int(args.seed))
    else:
        for i in range(args.iterations):
            seed = ri(0, 10**6 - 1)
            log.info('seed:  {:<6}, test#: {}'.format(seed, i))
            run(seed)
