import os
import errno
import logging
from collections import namedtuple
from os.path import basename, dirname, splitext, join
from glob import glob


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
    # Remember to edit if minimization-problem.
    try:
        with open(name + '.max', 'r') as f:
            return int(f.readline())
    except IOError:
        return 0


# Runs scoring function and checks if score is improved.
def process(inp, out, seed, sc_fun, testcase, ignore=False, force=False):

    bsc = _get_best(testcase)

    sc = _score(inp, out, sc_fun, ignore=ignore)

    fmt = 'score: {:<20}'
    if sc > bsc or force:
        fname = fname_fmt.format(testcase=testcase, score=sc, seed=seed)
        _save_ans(fname, 'ans', out)
        _save_ans(testcase, 'submission', out)

    if sc > bsc:
        logging.critical((fmt + " BEST! Improved by: {}").format(sc, sc - bsc))

        with open(testcase + '.max', 'w') as f:
            f.write(str(sc))
    else:
        logging.warn(fmt.format(sc))


fname_fmt = "{testcase}_{score}_{seed}"
