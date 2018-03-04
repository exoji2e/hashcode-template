# Template for Google Hash Code
to make it easier to deploy an incremental approach

To see an example of usage of this template 
(commit [2fe1063](https://github.com/exoji2e/hashcode-template/commit/2fe106309cec654289c73a217df904a509264b59))
look at Cache Flow's [solution](https://github.com/exoji2e/hashcode2018-qualification)
to the 2018 qualifier. Most forks are also usages of the template.

Run a testinstance on the format `in/$testcase.in` with your own solver by:

`python main.py --nsspec $file:$score:$solve $testcase` where 
- `$file` is the file with your functions `$score` and `$solve`
- `$score` is the function name of your scoring function
- `$solve` is the function name of your solution function

If you don't give `main` the `--nsspec` argument, the default is set to `solve:score:solve`, so you can just start working in `solve.py`.

`main.py` will handle file-io, save the solution that gets maximal score to the `submission`-folder, set up logging, set up randomization, etc.

## Nice to have for the competition:
- `pypy2` faster execution, because of JiT compilation to C
    + `brew install pypy`
- `sortedcontainers` sorted datastructures for greedy approaches:
    + `pypy -m pip install sortedcontainers`
