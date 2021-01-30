import os
import sys
import errno
import logging
import traceback
import datetime
from collections import namedtuple
from os.path import basename, dirname, splitext, join
from glob import glob
import subprocess
from importlib import import_module
from dataparser import parse2json


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

def sanitize_module_name(module_name):
    if module_name.endswith('.py'):
        module_name = module_name[:-3]
    module_name = module_name.replace('/', '.')
    return module_name


def get_function(section, config):
    orig_module_name = config.get(section, 'module')
    module_name = sanitize_module_name(orig_module_name)
    fun_name = config.get(section, 'function')
    try:
        module = import_module(module_name)
    except ModuleNotFoundError:
        raise ValueError(f"[{section}]: Can't find module {module_name} -  original module text: {orig_module_name}")
    try:
        return getattr(module, fun_name)
    except AttributeError:
        raise ValueError(f"[{section}]: Can't find function {fun_name} in module {module_name}")



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
            pass_inp = config['solve'].get('pass_input')
            if pass_inp == 'json':
                inp_blob = parse2json(inp)
            else:
                inp_blob = inp
            p.stdin.write(inp_blob.encode('ascii'))
            out, _ = p.communicate()
            return out.decode('ascii')
    return get_ans

def setup_run_folder(argv, config):
    now = str(datetime.datetime.now()).replace(' ', 'T').replace(':','-')
    folder = 'runs/{}'.format(now)
    mkdir(folder)

    open('{}/cmd.sh'.format(folder), 'w').write(' '.join(argv) + '\n')
    
    module_name = config.get('solve', 'module')
    if module_name.endswith('.py'):
        module_name = module_name[:-3]
    module_path = module_name.replace('.', '/') + '.py'
    os.system('cp {} {}/'.format(module_path, folder))

    return folder

def save_tmp_ans(folder, testcase, ans_id, ans):
    open('{}/{}_{}.ans'.format(folder, testcase, ans_id), 'w').write(ans)

def score2str(sc):
    def simple_sc_str(sc):
        for pw, letter in [(10**9, 'G'), (10**6, 'M'), (10**3, 'K')]:
            if sc >= pw:
                return '({:.2f}{})'.format(sc/pw, letter)
        return '({})'.format(sc)
    return '{:>10} {:>10}'.format(sc, simple_sc_str(sc))



def process(inp, out, solve_args, sc_fun):
    testcase = solve_args['testcase']
    folder = solve_args['folder']
    bsc = _get_best(testcase)

    try:
        logging.debug(f'Scoring output...')
        sc = _score(inp, out, sc_fun)
    except Exception as e:
        print('Scorer crashed!')
        traceback.print_exc()

    sc_str = score2str(sc)

    prev_sc_str = 'prev sc: {}'.format(score2str(bsc))
    now_sc_str =  'now  sc: {}'.format(score2str(sc))
    fname = fname_fmt.format(
        testcase=testcase,
        score=sc,
        seed=solve_args['seed'])

    logging.info(prev_sc_str)

    _save_ans(fname, folder, out)
    if sc > bsc:
        _save_ans(fname, 'ans', out)
        _save_ans(testcase, 'submission', out)


    if sc > bsc:
        extra = ' BEST! Improved by: {}'.format(score2str(sc - bsc))
        logging.critical(now_sc_str + extra)
        _update_best(testcase, sc, folder)
    else:
        logging.warn(now_sc_str)


fname_fmt = "{testcase}_{score}_{seed}"
