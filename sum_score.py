#!/user/bin/env pypy3
import glob
from util import score2str
import json
from pathlib import Path
import argparse

def get_args():
    examples = """
python3 sum_score.py
python3 sum_score.py artifacts/*_max.json
"""
    parser = argparse.ArgumentParser(
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('max_files', nargs='*')
    return parser.parse_args()

args = get_args()
if args.max_files:
    paths = args.max_files
else:
    paths = ['max.json']

def loadj(text):
    try:
        return json.loads(text)
    except:
        return {}

all_results = [(p, loadj(Path(p).read_text())) for p in paths]
collated = {}
for (p, maxjson) in all_results:
    for name, v in maxjson.items():
        if name not in collated or v['score'] > collated[name]['score']:
            collated[name] = v
            collated[name]['path'] = p

j = collated

S = 0
for name in sorted(j.keys()):
    v = j[name]['score']
    p = j[name]['path']
    m = j[name]['module']
    who_max = Path(p).with_suffix('').name
    print('{:25}: {:22} {:15} {}'.format(name, score2str(v), m, Path(p).name))
    S += v
print('{:25}: {:20}'.format('Total', score2str(S)))
