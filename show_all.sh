#!/bin/bash
for f in in/*.in; do
    echo '========================================'
    echo $f
    pypy show.py $f
done
