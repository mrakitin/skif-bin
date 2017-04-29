#!/bin/bash

if [ -z "$1" ]; then
    echo "  WARNING!!! There is no directories to process. Exiting..."
    exit 1
fi

idir=$PWD
dirs=$@

all_fermi_energies=$(for i in $dirs; do echo -e "\n$i"; grep :FER $i/$i.scf | tail -1; done)
max_energy=$(echo "$all_fermi_energies" | grep ":FER  : F E R M I - ENERGY(TETRAH.M.)=" | cut -d= -f2 | awk '{print $1}' | sort | tail -1)
echo -e "Maximum Fermi energy is: $max_energy\n"


for i in $dirs; do
    unset Eup Edn
    cd $i
    pwd
    configure_int -b total end >/dev/null 2>&1
    dE=$(cat $(basename $PWD).int | head -2 | tail -1 | awk '{print $2}')
    echo "dE = $dE"
    for updn in up dn; do
        unset outfile dosfile tmp lines_num

        outfile=$i.Efermi_$updn
        rm -fv $outfile
        dosfile=$i.dos1$updn
        rm -fv $dosfile 
        x tetra -$updn
        tmp=$(cat $dosfile | awk '{print $1,$2}' | grep -v "\#")
        lines_num=$(cat $dosfile | wc -l)

        sum=0
        for ((j=1; j<=${lines_num}; j++)); do
            unset a b c current_line
            current_line=$(echo "$tmp" | head -$j | tail -1)
            a=$(echo "scale=8; $(echo "$current_line" | awk '{print $1}')" | bc)
            b=$(echo "$current_line" | awk '{print $2}')
            if [ $(echo "$a <= $max_energy" | bc) = 1 ]; then
                c=$(echo "scale=8; $a * $b * $dE" | bc)
                sum=$(echo "scale=8; $sum + $c" | bc)
                echo "j = $j; a = $a; b = $b; c = $c; sum = $sum" >> $outfile
            else
                break
            fi
        done
        if [ "$updn" = "up" ]; then
            Eup=$sum
        else
            Edn=$sum
        fi

        tail -1 $outfile
    done
    Etotal=$(echo "scale=8; $Eup + $Edn" | bc)
    echo  -e "=== Total energy till Fermi energy for $i: $Etotal\n"

    cd $idir
    echo ""
done

exit 0

