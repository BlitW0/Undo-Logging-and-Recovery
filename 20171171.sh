#!/bin/bash

if [[ $# -eq 2 ]]; then
    python3 20171171_1.py "$1" "$2"
elif [[ $# -eq 1 ]]; then
    python3 20171171_2.py "$1"
else
    echo "Invalid number of arguments"
    echo "Usage for part1: ./20171171.sh <arg1> <arg2>"
    echo "Usage for part2: ./20171171 <arg1>"
fi
