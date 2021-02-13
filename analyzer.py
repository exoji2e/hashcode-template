#!/usr/bin/pypy3

from util import path
from dataparser import *
import json
import glob, argparse
import matplotlib
matplotlib.use('TkAgg') # sudo pacman -S tk # sudo apt install python3-tk
import matplotlib.pyplot as plt

def analyze(testcase, inp, ans):
    ns = parse(inp)
    print(f'Analyzing: {testcase}')
    itr = (line for line in ans.split('\n'))
    # TODO: Analyze the problem!
    # print(inp)
    

def analyze_wrap(run_folder, tc=None):
    in_f = glob.glob(f'{run_folder}/*.in')[0]
    ans_f = glob.glob(f'{run_folder}/*.ans')[0]
    with open(in_f) as f:
        inp = f.read()
    with open(ans_f) as f:
        ans = f.read()
    if tc == None:
        tc = path(in_f).name
    analyze(tc, inp, ans)

def get_run_folder(tc):
    p = path(tc)
    try:
        j = json.loads(open('max.json', 'r').read())
        return j[p.name]['folder']
    except:
        return None

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('testcase', nargs='?', default=None)
    parser.add_argument('-r', '--run_folder')
    parser.add_argument('-a', '--all', action='store_true')
    args = parser.parse_args()
    if args.all: return args
    if args.testcase:
        if args.run_folder: return args
        args.run_folder = get_run_folder(args.testcase)

    assert args.run_folder, 'need to provide all/testcase/run_folder'

    return args

def main():
    args = get_args()
    if args.all:
        for in_f in sorted(glob.glob('in/*.in')):
            tc = path(in_f).name
            r_f = get_run_folder(tc)
            if r_f == None:
                print('No runfolder in max.json for testcase {}'.format(tc))
                continue
            analyze_wrap(r_f, tc)
    else:
        r_f = args.run_folder
        analyze_wrap(r_f)


if __name__ == '__main__':
    main()



