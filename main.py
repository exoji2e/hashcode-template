from score import score
import sys
import random
from random import randint as ri
import logging as log
log.basicConfig(level=log.DEBUG, format='%(relativeCreated)6d %(message)s')

testcase = sys.argv[1]

with open('in/' + testcase + '.in') as f:
    lines = f.readlines()
### TODO: Proccess input data ###


# Runs scoring function and checks if score is improved.
def process(out, seed):
    sc = score(out)
    f = open(testcase+ '.max', 'r')
    bsc = int(f.readline())
    f.close()
    if sc > bsc:
        log.critical('New best score {} for testcase {}'.format(sc, testcase))
        fname = '_'.join([testcase, str(sc), seed]) + '.ans'
        f = open(testcase + '.max', 'w')
        f.write(str(sc))
        f.close()
        with open('ans/' + fname, 'w') as f:
            # Print to f
            f.write(str(out))
    else:
        log.warn('Score: {}'.format(sc))

def greedy(seed):
    #TODO: Solve the problem

    process(0, seed)

for i in range(10):
    seed = random.randint(0, 10000)
    log.info('seed: {}, test#: {}'.format(seed, i))
    greedy(seed)
