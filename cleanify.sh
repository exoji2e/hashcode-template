#!/bin/bash

function rm_nice {
    if [ -e $1 ] ; then
        rm $1
    fi
}
rm_nice "in"/*pizza*
rm_nice "max.json"
for f in "in"/* ; do
    if [ ${f: -4} == ".txt" ] ; then
        mv $f "${f%.txt}.in"
    fi
done
cp default.cfg main.cfg
