#!/usr/bin/env pypy3
import argparse, sys
import logging as log
from random import randint as ri
from util import update_config, get_function, path, process, get_ans_fn, setup_run_folder, sanitize_module_name, get_in_file_content
import glob
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
    examples = """
python3 main.py in/a_example.in
python3 main.py --solve module=solve_greedy.py --solve_args K=1,N=10 --all
"""

    parser = argparse.ArgumentParser(
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter
        )
    parser.add_argument('testcase', nargs='?', default=None)
    parser.add_argument('-a', '--all', action='store_true', help='run all input files located inside folder \'in/\'')
    parser.add_argument('-l', '--log', default='info', choices=loglvls.keys(), help="set the log level")
    parser.add_argument('-s', '--seed', default=None, help="provide a seed for the rng")
    parser.add_argument('-n', '--iterations', type=int, default=1, help="number of iterations to run the solver")
    parser.add_argument('-c', '--config', action='store', default='', help="config file")
    parser.add_argument('--score', action='store', default='', help="set scoring config, format: key1=value1,key2=value2")
    parser.add_argument('--solve', action='store', default='', help="set solve config, format: key1=value1,key2=value2")
    parser.add_argument('--solve_args', action='store', default='', help="set args for solve, format: key1=value1,key2=value2,...,keyN=valueN")
    args = parser.parse_args()
    if args.testcase == None and not args.all:
        parser.error('Either provide testcase or specify all with \'--all\'')
    return args



def init_log(testcase):
    for handler in log.root.handlers[:]:
        log.root.removeHandler(handler)
    fmt_str = '%(relativeCreated)6d {testcase:.3} %(filename).10s:%(lineno)-3d %(message)s'
    log.basicConfig(
        level=loglvls[args.log],
        format=fmt_str.format(testcase=testcase)
        )

def setup_stdstreams(run_folder):
    stdout = open('{}/stdout.log'.format(run_folder), 'w')
    stderr = open('{}/stderr.log'.format(run_folder), 'w')
    sys.stdout = Tie([sys.__stdout__, stdout])
    sys.stderr = Tie([sys.__stderr__, stderr])
    def tear_down():
        stdout.close()
        stderr.close()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
    return tear_down



def run_testcase(testcase, args):
    testcase = path(testcase).name
    config = ConfigParser()
    config.read(['default.cfg', 'main.cfg', args.config])

    update_config(config, 'score', args.score)
    update_config(config, 'solve', args.solve)

    sc_fn = get_function('score', config)
    run_folder = setup_run_folder(sys.argv, config, testcase)
    init_log(testcase)
    tear_down_streams = setup_stdstreams(run_folder)

    log.debug('Running testcase {}'.format(testcase))

    inp = get_in_file_content(testcase)
    solve_args = {}
    for kv in args.solve_args.split(','):
        if '=' in kv:
            k, v = kv.split('=')
            solve_args[k] = v
    solve_args['log'] = log
    solve_args['testcase'] = testcase
    solve_args['folder'] = run_folder
    orig_module_name = config.get('solve', 'module')
    solve_args['module_name'] = sanitize_module_name(orig_module_name)

    get_ans = get_ans_fn(config, inp)

    def run(solve_args):
        solve_args_orig = dict(solve_args)
        ans = get_ans(solve_args)
        process(inp, ans, solve_args_orig, sc_fn)

    rounds = 1 if args.seed else args.iterations
    for i in range(rounds):
        seed = args.seed if args.seed else ri(0, 10**6 - 1)
        log.debug('seed:  {:<6}, test#: {}'.format(seed, i))
        sa = dict(solve_args)
        sa['iter'] = i
        sa['seed'] = seed
        run(sa)

    tear_down_streams()



loglvls = {'debug': log.DEBUG, 'info': log.INFO, 'warning': log.WARNING, 'error': log.ERROR, 'critical': log.CRITICAL}
if __name__ == '__main__':
    args = get_args()
    if args.testcase:
        run_testcase(args.testcase, args)
    else:
        testcases = sorted(glob.glob('in/*.in'))
        for tc in testcases:
            run_testcase(tc, args)
