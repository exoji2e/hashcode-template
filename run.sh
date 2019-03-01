#!/bin/bash
for f in in/*.in; do
    echo $f
    pypy main.py $f
done
pypy sum_score.py
