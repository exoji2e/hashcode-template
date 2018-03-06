#!/usr/bin/env pypy
import argparse
import logging as log
from random import randint as ri
from util import update_config, get_function, path, process
from ConfigParser import ConfigParser


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('testcase')
    parser.add_argument('-l', '--log', default='debug', choices=loglvls.keys(), help="set the log level")
    parser.add_argument('-s', '--seed', default=None, help="provide a seed for the rng")
    parser.add_argument('-n', '--iterations', type=int, default=1, help="number of iterations to run the solver")
    parser.add_argument('-i', '--ignore', action='store_true', help="do not fail on scoring errors")
    parser.add_argument('-f', '--force', action='store_true', help="force output of result (overwrites ans file in submissions folder)")
    parser.add_argument('-c', '--config', action='store', default='', help="config file")
    parser.add_argument('--score', action='store', default='', help="set scoring config, format: key1=value1,key2=value2")
    parser.add_argument('--solve', action='store', default='', help="set solve config, format: key1=value1,key2=value2")
    return parser.parse_args()


def init_log():
    logfmt = config.get('log', 'log_fmt', 1).format(testcase=args.testcase)
    log.basicConfig(level=loglvls[args.log], format=logfmt)


loglvls = {'debug': log.DEBUG, 'info': log.INFO, 'warning': log.WARNING, 'error': log.ERROR, 'critical': log.CRITICAL}
if __name__ == '__main__':
    args = get_args()
    args.testcase = path(args.testcase).name
    config = ConfigParser()
    config.read(['main.cfg', args.config])
    init_log()

    update_config(config, args.score)
    update_config(config, args.solve)

    sc_fn = get_function('score', config)
    sol_fn = get_function('solve', config)

    with open('in/' + args.testcase + '.in') as f:
        inp = f.read()

    def run(seed):
        ans = sol_fn(seed, inp, log)
        process(inp, ans, seed, sc_fn, args.testcase, ignore=args.ignore, force=args.force)

    if args.seed:
        log.info('seed: {}'.format(args.seed))
        run(int(args.seed))
    else:
        for i in range(args.iterations):
            seed = ri(0, 10**6 - 1)
            log.info('seed:  {:<6}, test#: {}'.format(seed, i))
            run(seed)
