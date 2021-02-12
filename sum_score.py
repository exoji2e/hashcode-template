#!/user/bin/env pypy3
import glob
from util import path, score2str
try:
    import json
    j = json.loads(open('max.json', 'r').read())
except:
    j = {}

S = 0
for name in sorted(j.keys()):
    v = j[name]['score']
    f = j[name]['folder']
    pys = glob.glob('{}/*.py'.format(f))
    sol_name = ''
    if pys:
        sol_name = ' '.join(path(pyf).name for pyf in pys)
    print('{:25}: {:20} {:20} {}'.format(name, score2str(v), sol_name, f))
    S += v
print('{:25}: {:20}'.format('Total', score2str(S)))
