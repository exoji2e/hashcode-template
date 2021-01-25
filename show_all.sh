#!/bin/bash
for f in in/*.in; do
    echo '========================================'
    echo $f
    pypy3 show.py $f
done
