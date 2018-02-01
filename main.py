import argparse
import logging as log
from random import randint as ri
from util import mkdir
from os import link, remove


# Runs scoring function and checks if score is improved.
def process(inp, out, seed, sc_fun):

    # Remember to edit if minimization-problem.
    try:
        with open(args.testcase + '.max', 'r') as f:
            bsc = int(f.readline())
    except IOError:
        bsc = 0

    sc = sc_fun(inp, out)

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
        link(fpath, latest)
    else:
        log.warn(fmt.format(sc))


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('testcase')
    parser.add_argument('-l', '--log', default='debug')
    parser.add_argument('-s', '--seed', default=None)
    parser.add_argument('-n', '--iterations', type=int, default=10)
    parser.add_argument('--nsspec', action='store', default="solve:score:solve")
    return parser.parse_args()


def init_log():
    loglvls = {'debug': log.DEBUG, 'info': log.INFO, 'warning': log.WARNING, 'error': log.ERROR, 'critical': log.CRITICAL}
    logfmt = '%(relativeCreated)6d {} %(filename)12s:%(lineno)-3d %(message)s'.format(args.testcase)
    log.basicConfig(level=loglvls[args.log], format=logfmt)


if __name__ == '__main__':
    args = get_args()
    init_log()
    nsspec = args.nsspec.split(":")
    sol_module = nsspec[0]
    score_fun_name = "score"
    solve_fun_name = "solve"
    if len(nsspec) > 2:
        score_fun_name = nsspec[1]
        solve_fun_name = nsspec[2]

    sol = __import__(sol_module, globals(), locals(), [], 0)
    sc_fn = getattr(sol, score_fun_name)
    sol_fn = getattr(sol, solve_fun_name)

    with open('in/' + args.testcase + '.in') as f:
        inp = f.read()

    def run(seed):
        ans = sol_fn(seed, inp, log)
        process(inp, ans, seed, sc_fn)

    if args.seed:
        log.info('seed: {}'.format(args.seed))
        run(args.seed)
    else:
        for i in range(args.iterations):
            seed = ri(0, 10**6 - 1)
            log.info('seed:  {:<6}, test#: {}'.format(seed, i))
            run(seed)
