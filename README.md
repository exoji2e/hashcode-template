# Template for Google Hash Code
to make it easier to deploy an incremental approach. _Automating the booring parts._

To see an (possibly a bit out of date) example usage of this template 
(commit [2fe1063](https://github.com/exoji2e/hashcode-template/commit/2fe106309cec654289c73a217df904a509264b59))
look at Cache Flow's [solution](https://github.com/exoji2e/hashcode2018-qualification)
to the 2018 qualifier. Most forks are also usages of the template.

## Model:
- `solvers/solve.py` should implement the function `solve` that takes the input as a string and returns an answer as a string.
- `score.py` should implement a function `score` that takes the input as `solve` got, and what `solve` returned, and then scores the submission. You should return the score as an integer.
- Parsing of the input-file is done to an `argparse.NameSpace` in `dataparser.py` 
- `main.py` reads the config files `default.cfg`, `main.cfg` and then the commandline argument applied config file, in that order, overwriting config-elements if the file exists. It then runs the scorer and solver that are specified. Each time you invoke `main.py` a folder inside `runs/` is created with relevant data about your run.


 If you get a higher score than before on a test case the submission is saved in the `submission` folder, and a link to the run folder is created in the folder `best_runs/`.

Run a testinstance on the format `in/$testcase.in` with your own solver by:

`python main.py $testcase`, given that you have implemented the functions `solve` in `solvers/solve.py` and `score` in `score.py`. If you want to name your files, solve and score-functions differently the module and function-names in the config-file `default.cfg` can be modified, or set directly by arguments. For example if you want to run the pizza-solution, which has `solve` and `score` functions implemented in the module `pizza.py`, do `python main.py -c tests/pizza.cfg in/exaple_pizza.in` or manually `python main.py --score module=tests/pizza --solve module=tests/pizza in/example_pizza.in`

`main.py` will handle file-io, save the solution that gets maximal score to the `submission`-folder, set up logging, set up randomization, etc.

## Other functionality:
- `sum_score.py` - looks in `max.json` and prints a table with a row for each input file: `{testcase} {max_score} {solve_module used} {run_folder_w_high_score}`
- `show.py` - easy access to the input files to do visualizations of them.
- `analyze.py` - easy access to the run folders and best run folder to analyze the output-file.
- Bug in your scorer? Just remove `max.json` and rerun, now main.py will happliy overwrite the ans-files in the `submission` folder. If you accidentaly remove `max.json` you can recover your ans files form the `best_runs` folder or the `ans` folder.
- `package.sh` create a zip folder with your solution
- `setup.sh` removes `in/example_pizza.in` and creates a main.cfg.
- Pass extra args to your solver with: `pypy3 main.py --solve_args N=10,M=Hello,X=-0.5` Filling the args-dict with `{"N" : "10", "M" : "Hello", "X" : "-0.5"}`.


## How my team uses this:
We start by implementing a solver and a scorer in parallel. Usually we try to make a very dumb solver to have a baseline for improvements. After we have a system working were we get a score and the judge system reports the same score we continue on 2 or three different solvers that do things differently. Usually we opt for different greedy approaches that sort of different _reasonable_ weight funtions.

A good idea is also to create an _improver_ that you can apply after any solver. However it depends on the problem if there exists a reasonable improver. For the pizza problem there exists an improver that expands all the small pizza pieces, which usually gives quite a few extra points, depending on your solution.

Another good idea is to analyze your inputs and outputs. `show.py` and `analyze.py` helps out with file-io. If you wish to use `matplotlib`, remember that it's easier used under `python3` than `pypy3`.

## Nice to have for the competition:
- `pypy3` faster execution, because of JiT compilation to C
    + MacOS: `brew install pypy3`
    + Ubuntu: `sudo apt-get install pypy3`
    + Arch: `sudo pacman -S pypy3`
- `sortedcontainers` sorted datastructures for greedy approaches:
    + `pypy3 -m pip install sortedcontainers`
- `matplotlib` for drawing charts/grids visualizing inputs/outputs.
    + `python3 -m pip install matplotlib`
- Your own gitrepo to share your progress with your team mates. Just clone this repo and upload you your own private repo.

Have any questions? Post an issue here or tweet to @exoji2e.
