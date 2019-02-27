# Template for Google Hash Code
to make it easier to deploy an incremental approach

To see an example of usage of this template 
(commit [2fe1063](https://github.com/exoji2e/hashcode-template/commit/2fe106309cec654289c73a217df904a509264b59))
look at Cache Flow's [solution](https://github.com/exoji2e/hashcode2018-qualification)
to the 2018 qualifier. Most forks are also usages of the template.

## Model:
- `solve.py` should implement the function `solve` that takes the input as a string and returns an answer as a string.
- `score.py` should implement a function `score` that takes the input as `solve` got, and what `solve` returned, and then scores the submission. You should return the score as an integer.
- `main.py` reads the config file `main.cfg` (or takes cmd-line arguments) and runs the scorer and solver that are specified. If you get a higher score than before on a test case the submission is saved in the `submission` folder, and the `ans` folder.

Run a testinstance on the format `in/$testcase.in` with your own solver by:

`python main.py $testcase`, given that you have implemented the functions `solve` in `solve.py` and `score` in `score.py`. If you want to name your files, solve and score-functions differently the module and function-names in the config `main.cfg` can be modified, or set directly by arguments. For example if you want to run the pizza-solution, which has `solve` and `score` functions implemented in the module `pizza.py`, do `python main.py -c pizza.cfg in/exaple_pizza.in` or manually `python main.py --score module=pizza --solve module=pizza in/example_pizza.in`

`main.py` will handle file-io, save the solution that gets maximal score to the `submission`-folder, set up logging, set up randomization, etc.

## How my team uses this:
We start by implementing a solver and a scorer in parallel. Usually we try to make a very dumb solver to have a baseline for improvements. After we have a system working were we get a score and the judge system reports the same score we continue on 2 or three different solvers that do things differently. Usually we opt for different greedy approaches that sort of different _reasonable_ weight funtions.

A good idea is also to create an _improver_ that you can apply after any solver. However it depends on the problem if there exists a reasonable improver. For the pizza problem there exists an improver that expands all the small pizza pieces, which usually gives quite a few extra points, depending on your solution.

## Nice to have for the competition:
- `pypy2` faster execution, because of JiT compilation to C
    + MacOS: `brew install pypy`
    + Ubuntu: `sudo apt-get install pypy`
- `sortedcontainers` sorted datastructures for greedy approaches:
    + `pypy -m pip install sortedcontainers`
