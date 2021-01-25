#!/bin/bash
for f in in/*.in; do
    echo $f
    pypy3 main.py $f
done
pypy3 sum_score.py
