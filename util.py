import os
import errno
import logging
import datetime
from collections import namedtuple
from os.path import basename, dirname, splitext, join
from glob import glob
import subprocess


SimplePath = namedtuple('Path', ['dir', 'name', 'ext'])


class Path(SimplePath):
    def read(self):
        with open(str(self), 'r') as f:
            return f.read()

    def __str__(self):
        return(join(*self[:2]) + self.ext)

    def rename(self, name):
        new_path = Path(self.dir, name, self.ext)
        os.rename(str(self), str(new_path))
        return new_path


def get_function(section, config):
    module_name = config.get(section, 'module')
    fun_name = config.get(section, 'function')
    module = __import__(module_name, globals(), locals(), [], 0)
    return getattr(module, fun_name)


def update_config(config, config_part, update_str):
    for k, v in (e.split('=') for e in update_str.split(',') if e):
        config.set(config_part, k, v)


def path(fname):
    base = basename(fname)
    dirn = dirname(fname)
    return Path(dirn, *splitext(base))


def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def clean_max():
    for fname in glob('./*.max'):
        os.remove(fname)


def _save_ans(fname, subdir, out):
        mkdir(subdir)
        latest = "{}/{}.ans".format(subdir, fname)
        with open(latest, 'w') as f:
            f.write(str(out))


def _score(inp, out, sc_fun, ignore=False):
    try:
        return sc_fun(inp, out)
    except Exception as e:
        if not ignore:
            raise
        logging.error(str(e))
        return 0

def _get_best(name):
    try:
        import json
        j = json.loads(open('max.json', 'r').read())
        return j[name]['score']
    except:
        # Edit if minimization problem
        return 0


def _update_best(name, score, run_folder):
    try:
        import json
        with open('max.json', 'r') as f:
            j = json.loads(f.read())
    except:
        j = {}
    if name not in j:
        j[name] = {}
    j[name]['score'] = score
    j[name]['folder'] = run_folder
    f = open('max.json', 'w')
    f.write(json.dumps(j))
    f.close()


def get_ans_fn(config, inp):
    try:
        run_cmd = config.get('solve', 'run')
    except:
        run_cmd = None
    if run_cmd == None:
        sol_fn = get_function('solve', config)
        def get_ans(solve_args):
            ans = sol_fn(inp, solve_args)
            return ans
    else:
        def get_ans(solve_args):
            p = subprocess.Popen(run_cmd.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            p.stdin.write(inp.encode('ascii'))
            out, _ = p.communicate()
            return out.decode('ascii')
    return get_ans

def setup_run_folder(argv, config):
    now = str(datetime.datetime.now()).replace(' ', 'T').replace(':','-')
    folder = 'runs/{}'.format(now)
    mkdir(folder)

    open('{}/cmd.sh'.format(folder), 'w').write(' '.join(argv) + '\n')
    
    module = config.get('solve', 'module')
    module_path = module.replace('.', '/') + '.py'
    os.system('cp {} {}/'.format(module_path, folder))

    return folder

def save_tmp_ans(folder, testcase, ans_id, ans):
    open('{}/{}_{}.ans'.format(folder, testcase, ans_id), 'w').write(ans)


def process(inp, out, solve_args, sc_fun):
    testcase = solve_args['testcase']
    folder = solve_args['folder']
    bsc = _get_best(testcase)

    sc = _score(inp, out, sc_fun)

    fmt = 'score: {:<20}'
    fname = fname_fmt.format(testcase=testcase, score=sc, seed=solve_args['seed'])
    _save_ans(fname, folder, out)
    if sc > bsc:
        _save_ans(fname, 'ans', out)
        _save_ans(testcase, 'submission', out)

    if sc > bsc:
        logging.critical((fmt + " BEST! Improved by: {}").format(sc, sc - bsc))
        _update_best(testcase, sc, folder)
    else:
        logging.warn(fmt.format(sc))


fname_fmt = "{testcase}_{score}_{seed}"
