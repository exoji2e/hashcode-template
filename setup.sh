#!/bin/bash
mkdir -p ans
cd "in"

for f in *.in; do
    name=${f%'.in'}
    if [ ! -f "../$name.max" ]; then
        echo 0 > "../$name.max"
    fi
done
