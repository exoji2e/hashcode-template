#!/usr/bin/env pypy
import argparse, sys
import logging as log
from random import randint as ri
from util import update_config, get_function, path, process, get_ans_fn, setup_run_folder
try:
    from ConfigParser import ConfigParser
except:
    from configparser import ConfigParser

class Tie:
    def __init__(self, out_streams):
        self.out_streams = out_streams
    def write(self, s):
        for o in self.out_streams:
            o.write(s)
    def close(self):
        for o in self.out_streams:
            o.close()
    def flush(self):
        for o in self.out_streams:
            o.flush()

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
    parser.add_argument('--solve_args', action='store', default='', help="set args for solve, format: key1=value1,key2=value2,...,keyN=valueN")
    return parser.parse_args()


def init_log():
    fmt_str = '%(relativeCreated)6d {testcase:.3} %(filename).10s:%(lineno)-3d %(message)s'
    log.basicConfig(level=loglvls[args.log], format=fmt_str.format(testcase=args.testcase))


loglvls = {'debug': log.DEBUG, 'info': log.INFO, 'warning': log.WARNING, 'error': log.ERROR, 'critical': log.CRITICAL}
if __name__ == '__main__':
    args = get_args()
    args.testcase = path(args.testcase).name
    config = ConfigParser()
    config.read(['default.cfg', 'main.cfg', args.config])

    update_config(config, 'score', args.score)
    update_config(config, 'solve', args.solve)

    sc_fn = get_function('score', config)

    run_folder = setup_run_folder(sys.argv, config)

    with open('in/' + args.testcase + '.in') as f:
        inp = f.read()
    solve_args = {}
    for kv in args.solve_args.split(','):
        if '=' in kv:
            k, v = kv.split('=')
            solve_args[k] = v
    solve_args['log'] = log
    solve_args['testcase'] = args.testcase
    solve_args['folder'] = run_folder
    stdout = open('{}/stdout.log'.format(run_folder), 'w')
    stderr = open('{}/stderr.log'.format(run_folder), 'w')
    sys.stdout = Tie([sys.__stdout__ , stdout])
    sys.stderr = Tie([sys.__stderr__, stderr])

    init_log()

    get_ans = get_ans_fn(config, inp)

    def run(solve_args):
        solve_args_orig = dict(solve_args)
        ans = get_ans(solve_args)
        process(inp, ans, solve_args_orig, sc_fn)

    if args.seed:
        log.info('seed: {}'.format(args.seed))
        sa = dict(solve_args)
        sa['iter'] = 0
        sa['seed'] = args.seed
        run(sa)
    else:
        for i in range(args.iterations):
            seed = ri(0, 10**6 - 1)
            log.info('seed:  {:<6}, test#: {}'.format(seed, i))
            sa = dict(solve_args)
            sa['iter'] = i
            sa['seed'] = seed
            run(sa)
