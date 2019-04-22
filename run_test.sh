#!/bin/bash
if [ $# == 1 ]; then
    echo "Running with quick parse. If real parse is existing, remove the argument."
else
    echo "Running with real parse. If real parse is not ready, add qs as argument to run_test."
fi
for f in in/*.in; do
    echo $f
    if [ $#==1 ]; 
    then 
        pypy test_script.py $1 $f
    else
        pypy test_script.py $f
    fi
done
