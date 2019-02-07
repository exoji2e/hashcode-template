#!/bin/bash
for f in in/*.in; do
    name=$(echo $f | sed "s/in//g" | sed "s/[\.\/]//g")
    echo $name
    pypy main.py $name
done
pypy sum_score.py
