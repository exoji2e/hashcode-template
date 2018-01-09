from score import score
import sys

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
        print('New best score {} for testcase {}'.format(str(sc), testcase))
        fname = '_'.join([testcase, str(sc), seed]) + '.ans'
        f = open(testcase + '.max', 'w')
        f.write(str(sc))
        f.close()
        with open('ans/' + fname, 'w') as f:

            # Print to f
            f.write(str(out))

def greedy(seed):
    # do greedy stuff

    process(0, seed)

greedy('greedy')
