import argparse
import random
import sys
sys.path.extend(['..', '.'])
from collections import *
from dataparser import parse
from util import get_in_file_content


def parse(inp):
    lines = inp.split('\n')
    R, C, L, H = map(int, lines[0].split())
    board = [list(map(lambda x: x=='T', line.strip())) for line in lines[1:]]
    return argparse.Namespace(r=R, c=C, l=L, h=H, board=board)


def score(inp, out):
    ns = parse(inp)
    used = [[False]*ns.c for _ in range(ns.r)]
    rects = [tuple(map(int, l.split())) for l in out.split('\n')[1:]]
    sc = 0
    for r in rects:
        sc += area(r)
        for x, y in coords(r):
            if used[x][y]:
                raise ValueError('rectangles overlaps')
            used[x][y] = True

    return sc


def area(r):
    return (r[2] - r[0] + 1)*(r[3] - r[1] + 1)


def dims(ns):
    for dx in range(1, ns.h+1):
        for dy in range(1, ns.h+1):
            A = dx*dy
            if ns.l*2 <= A <= ns.h:
                yield dx, dy


def coords(r):
    for x in range(r[0], r[2]+1):
        for y in range(r[1], r[3]+1):
            yield x, y


def ing(r, ns):
    t = 0
    for x, y in coords(r):
        if ns.board[x][y]: t+=1
    return t, area(r) - t


def solve(inp, args):
    random.seed(args['seed'])
    ns = parse(inp)
    rects = []
    for x1 in range(0, ns.r):
        for y1 in range(0, ns.c):
            for dx, dy in dims(ns):
                x2, y2 = x1 + dx-1, y1 + dy-1
                if x2 >= ns.r or y2 >= ns.c: continue
                r = (x1, y1, x2, y2)
                t, m = ing(r, ns)
                if min(t, m) >= ns.l:
                    rects.append(r)
    used = [[False]*ns.c for _ in range(ns.r)]
    random.shuffle(rects)
    pick = []
    for r in rects:
        ok = True
        for x, y in coords(r):
            ok = ok and not used[x][y]
        if not ok: continue
        for x, y in coords(r):
            used[x][y] = True
        pick.append(r)
    out = ["{} {} {} {}".format(*r) for r in pick]
    return '\n'.join([str(len(out))] + out)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('in_file')
    args = parser.parse_args()
    inp = get_in_file_content(args.in_file)
    out = solve(inp, {'seed': 0})
    print('\n'.join(['OUT:', '=========', out]))
