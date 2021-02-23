#!/bin/sh

if ! test -d "artifacts" ; then
    echo "folder artifacts is not present create a link first"
    exit 1
fi

initials=$1

echo "Initials: $initials"
best_runs="artifacts/$initials"_best_runs
max="artifacts/$initials"_max.json
echo "will touch and link best_runs -> $best_runs"
echo "will touch and link max.json -> $max"

read -p "Do you wish to continue? [y/N]: " -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]] ; then
    exit 1 
fi

set -x
mkdir -p $best_runs
touch $max
ln -s $best_runs best_runs
ln -s $max max.json