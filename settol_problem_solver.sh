#!/bin/bash

# The script is for solving a problem with sgroup routine of WIEN2k when using a structure after a minimization.
# Author: Maxim Rakitin
# Date: 2012-08-28 (Tue)

usage () {
cat << EOF

  Usage: $0 -i case.struct -n N
         N - a number of digits from the end of a coordinate to round down."

EOF

exit 1
}

########################## Arguments processing #########################
if [ ! -z "$1" ]; then
    unset struct num
    while [ "$#" -gt "0" ]; do
        arg=$1
        shift
        case $arg in
            -i | -input)
                struct=$1
                shift
            ;;
            -n | -number)
                num="$1"
                shift
            ;;
            -h | -help | --help)
                usage
            ;;
            -usage)
                usage
            ;;
        esac
    done
else
    usage
fi

if [ -z "$struct" ]; then
    usage
fi

if [ -z "$num" ]; then
    num=4
    echo "  The default value of N will be used: $num"
else
    if [ "$num" -gt 0 -a "$num" -lt "8" ]; then
        echo "  The following value of N will be used: $num"
    else
        echo "  WARNING!!! The number of digits can be in range [1; 7]! Exiting..."
        exit 2
    fi
fi

unset dots_list zeros_list
for ((i=1; i<=$num; i++)); do
    dots_list="${dots_list}."
    zeros_list="${zeros_list}0"
done

#echo "=== dots_list = $dots_list; zeros_list = $zeros_list"



crd_list=$(echo $(grep "X=" $struct | cut -d= -f2,3,4 | sed 's/Y=//g; s/Z=//g; s/ /\n/g;' | sort | uniq))

for i in $crd_list; do
    unset crd_sed
    crd_sed=$(echo $i | sed 's/'"$dots_list"'$/'"$zeros_list"'/g')
    echo -e "$i ---> $crd_sed"

    if [ -z "$crd_sed" ]; then
        echo "  WARNING!!! Coordinates from $struct cannot be processed."
        exit 3
    fi
    sed 's/'"$i"'/'"$crd_sed"'/g' -i $struct
done


exit 0

