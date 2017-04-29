#!/bin/bash

# VASP calculations

idir=$PWD

for name in *.vasp; do
    echo -e "\n\n$name"

    calc_dir=$(echo $name | sed 's/.vasp//g')
    if [ ! -d "$calc_dir" ]; then
	mkdir -v $calc_dir
    fi

    cd $calc_dir
    pwd
    
    cp -v ../$name POSCAR
    cat /dev/null > POTCAR
    for i in $(cat POSCAR | head -6 | tail -1); do
	echo $i
	echo POTCAR_${i}
	cat ../../POTCARS/POTCAR_${i} >> POTCAR
    done

    cp -v ../../INCAR .
    sed -i 's/SYSTEM =/SYSTEM = '"$calc_dir"'/g' INCAR
    
    cp -v ../../job $calc_dir.job
    short_name=$(echo $calc_dir | sed 's/53//g')
    sed -i 's/#BSUB -J/#BSUB -J  '"$short_name"'/g' $calc_dir.job

    if [ "$1" == 'sub' ]; then
	bsub < $calc_dir.job
    fi

    cd $idir
done

