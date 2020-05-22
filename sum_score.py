#!/bin/python
try:
    import json
    j = json.loads(open('max.json', 'r').read())
except:
    j = {}

S = 0
for name in sorted(j.keys()):
    v = j[name]['score']
    f = j[name]['folder']
    print('{}: {} {}'.format(name, v, f))
    S += v
print('Total: {}'.format(S))
