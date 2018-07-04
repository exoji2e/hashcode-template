# Template for Google Hash Code
to make it easier to deploy an incremental approach

To see an example of usage of this template 
(commit [2fe1063](https://github.com/exoji2e/hashcode-template/commit/2fe106309cec654289c73a217df904a509264b59))
look at Cache Flow's [solution](https://github.com/exoji2e/hashcode2018-qualification)
to the 2018 qualifier. Most forks are also usages of the template.

Run a testinstance on the format `in/$testcase.in` with your own solver by:

`python main.py $testcase`, given that you have implemented the functions `solve` in `solve.py` and `score` in `score.py`. If you want to name your files, solve and score-functions differently the module and function-names in the config `main.cfg` can be modified, or set directly by arguments. For example if you want to run the pizza-solution, which has `solve` and `score` functions implemented in the module `pizza.py`, do `python main.py -c pizza.cfg in/exaple_pizza.in` or manually `python main.py --score module=pizza --solve module=pizza in/example_pizza.in`

`main.py` will handle file-io, save the solution that gets maximal score to the `submission`-folder, set up logging, set up randomization, etc.

## Nice to have for the competition:
- `pypy2` faster execution, because of JiT compilation to C
    + `brew install pypy`
- `sortedcontainers` sorted datastructures for greedy approaches:
    + `pypy -m pip install sortedcontainers`
