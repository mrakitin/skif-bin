#!/bin/bash

# Purpose: find max energy of H peak in DOS of H (in region ~0.65 Ry)
# 2012-01-26

#if [ -z "$1" ]; then
#    echo "  WARNING!!! Please point input file. Exiting..."
#    exit 1
#fi

for updn in up dn; do
    unset infile DOS_interval first_E last_E E_vs_states max_values max_E max_states 
    infile=atom_55_H.$updn

    DOS_interval=$(cat $infile | head -1714 | tail -122)
    first_E=$(echo "${DOS_interval}" | head -1 | awk '{print $1}')
    last_E=$(echo "${DOS_interval}" | tail -1 | awk '{print $1}')

    #echo " First E value: $first_E"
    #echo " Last  E value: $last_E"

    E_vs_states=$(echo "$DOS_interval" | awk '{print $1, $3}')

    max_values=$(echo "${E_vs_states}" | awk '{print $2, $1}' | sort | tail -1)
    max_E=$(echo $max_values | awk '{print $2}')
    max_states=$(echo $max_values | awk '{print $1}')

    #echo " Max E        : $max_E"
    #echo " Max states   : $max_states"
    if [ "$updn" = "up" ]; then
         max_E_up=$max_E
    else
         max_E_dn=$max_E
    fi
done

idir=$PWD
cd ../..
#echo "  Current dir: $PWD"
calc_dir=$(basename $PWD)
alat_x3=$(head -4 ${calc_dir}.struct | tail -1 | awk '{print $1}')
Etotal=$(grep :ENE ${calc_dir}.scf | tail -1 | awk '{print $NF}')
CUP=$(grep :CUP ${calc_dir}.scf | tail -1 | awk '{print $NF}')
CDN=$(grep :CDN ${calc_dir}.scf | tail -1 | awk '{print $NF}')
CSum=$(echo "scale=8; $CUP + $CDN" | bc)
col_charge=$(echo "scale=8; 1 - $CSum" | bc)
#Ry2eV=13.6
Ry2eV=13.60569253
max_E_up_eV=$(echo "scale=8; $max_E_up * $Ry2eV * (-1)" | bc)
max_E_dn_eV=$(echo "scale=8; $max_E_dn * $Ry2eV * (-1)" | bc)
max_E_average=$(echo "scale=8; ($max_E_up_eV + $max_E_dn_eV)/2" | bc)

spheres_parser $(basename $PWD).struct > /dev/null 2>&1
pore_vol=$(det4x4 $(basename $PWD).1st_sphere | grep "Determinant is:" | cut -d: -f2 | awk '{print $1}')

# dndH = $col_charge * ($B2 * $max_E_average * (($B4)^0.5) * $B5 + $B6)/$B9 * $B8
B2="18.60"
B4="5.00"
B5="0.612"
B6="90.00"
B8="6.24151*(10^21)"
B9="6.22045*(10^23)"
B8_B9=$(echo "scale=8; 6.24151 / 6.22045 * 10^(-2)" | bc)
dndH=$(echo "scale=8; $col_charge * ($B2 * $max_E_average * sqrt($B4) * $B5 - $B6) * $B8_B9" | bc)


cd $idir

echo -e "$alat_x3 $pore_vol $Etotal $CUP $CDN $CSum $col_charge $max_E_up $max_E_dn $max_E_up_eV $max_E_dn_eV $max_E_average $dndH"

exit 0

