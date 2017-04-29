#!/bin/bash

idir=$PWD
free_nodes=$(echo $(pbsnodes | grep "state = free" -B1 | grep "n[0-9][0-9][0-9][0-9]\.cluster" | sort | uniq))
free_nodes_nocluster=$(echo $(pbsnodes | grep "state = free" -B1 | grep "n[0-9][0-9][0-9][0-9]\.cluster" | sort | uniq) | sed 's/\.cluster//g')
echo "Free nodes: ${free_nodes_nocluster}"
#exit 999

for i in ${free_nodes}; do
    cd $idir
    if [ -d "$i" ]; then
        rm -rf $i
    fi
    mkdir $i
    cp -v TEST.struct $i/$i.struct -v
    cd $i
    sed 's/TEST/'"$i"'/g' -i $(basename $PWD).struct
    qjob -n $i:12:300 -s runsp -lapw0 para -i 13:-7.0:3.5:24 -q
    sleep 5
done


exit 0

