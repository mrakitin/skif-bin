#!/bin/bash

module load compilers/cplusplus/intel/12.1.0

if [ -z "$1" ]; then
    echo "  WARNING!!! Please specify input file. Exiting..."
    exit 1
fi

if [ "$2" = "-v" ]; then
    verbose="-v"
else
    verbose=""
fi

input=$1
if [ -z "$(echo $input | grep cpp)" ]; then
    echo "  WARNING!!! The specified file $input is not correct. Use .cpp extension. Exiting..."
    exit 2
fi
output="$(echo $input | sed 's/\.cpp//g').exe"

icc $verbose $input -o $output

