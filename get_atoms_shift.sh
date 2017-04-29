#!/bin/bash
#
# The script gets atoms shift from their equilibrium positions using ideal structure coordinates.
# Author: Maxim Rakitin
# Date  : 2012-03-16

check_crd () {
    unset crd atoms_line field crd_value
    if [ ! -z "$1" ]; then
	local crd=$1
    else
	return 1
    fi
    if [ ! -z "$2" ]; then
	local atoms_line="$2"
    else
	return 1
    fi

    if [ "$crd" = "x" ]; then
	local field=2
    elif [ "$crd" = "y" ]; then
	local field=3
    elif [ "$crd" = "z" ]; then
	local field=4
    else
	return 1
    fi
    
    crd_value=$(echo $atoms_line | cut -d= -f$field | awk '{print $1}')
}

norm_crd () {
    unset crd norm_value
    if [ ! -z "$1" ]; then
        local crd=$1
    else
        return 1
    fi
    if [ "$(echo "$crd>=0.98" | bc)" = 1 ]; then
        norm_value=$(echo "scale=12; ($crd)-1" | bc | cut -c -10)
    else
	norm_value=$crd
    fi
}

calc_distance () {
    unset atom_one atom_two distance
    unset x1 y1 z1
    unset x2 y2 z2

    if [ ! -z "$1" ]; then
        local atom_one=$1
    else
        return 1
    fi
    if [ ! -z "$2" ]; then
        local atom_two="$2"
    else
        return 1
    fi

    check_crd x "$atom_one"; local x1=$crd_value
    check_crd y "$atom_one"; local y1=$crd_value
    check_crd z "$atom_one"; local z1=$crd_value

    check_crd x "$atom_two"; local x2=$crd_value
    check_crd y "$atom_two"; local y2=$crd_value
    check_crd z "$atom_two"; local z2=$crd_value

    norm_crd $x1; x1=$norm_value
    norm_crd $y1; y1=$norm_value
    norm_crd $z1; z1=$norm_value

    norm_crd $x2; x2=$norm_value
    norm_crd $y2; y2=$norm_value
    norm_crd $z2; z2=$norm_value

    distance=$(echo "scale=12; $alat * sqrt(($x1 - $x2)^2 + ($y1 - $y2)^2 + ($z1 - $z2)^2)" | bc)
}


#---> Real structure processing:
input_file=$1
if [ -z "$1" -o ! -f "$1" ]; then
    echo "  WARNING!!! The specified file is not correct. Exiting..."
    exit 1
fi

alat=$(cat $input_file | head -4 | tail -1 | awk '{print $1}')
current_crds=$(grep -e "^ATOM" $input_file)
atoms_num=$(echo "$current_crds" | wc -l)

impurity=$(grep Z: $input_file | awk '{print $1}' | sort | uniq | grep -ve "^Fe$" | grep -ve "^H$")
impurity_line=$(grep "Z:" -B2 $input_file | grep "$impurity" -B2 | head -1)
impurity_id=$(echo "$impurity_line" | awk '{print $2}' | sed 's/-//g; s/://g')


#---> Ideal structure processing:
# Ideal coordinates were taken from /home/max/calc/.docs/.structs/Fe54H_t.struct on skif-ural using the following commands:
# ideal_structure="/home/max/calc/.docs/.structs/Fe54H_t.struct"
# ideal_crds=$(grep -e "^ATOM" $ideal_structure)

ideal_crds="\
ATOM  -1: X=0.00000000 Y=0.00000000 Z=0.00000000
ATOM  -2: X=0.33333333 Y=0.00000000 Z=0.00000000
ATOM  -3: X=0.66666667 Y=0.00000000 Z=0.00000000
ATOM  -4: X=0.00000000 Y=0.33333333 Z=0.00000000
ATOM  -5: X=0.33333333 Y=0.33333333 Z=0.00000000
ATOM  -6: X=0.66666667 Y=0.33333333 Z=0.00000000
ATOM  -7: X=0.00000000 Y=0.66666667 Z=0.00000000
ATOM  -8: X=0.33333333 Y=0.66666667 Z=0.00000000
ATOM  -9: X=0.66666667 Y=0.66666667 Z=0.00000000
ATOM -10: X=0.00000000 Y=0.00000000 Z=0.33333333
ATOM -11: X=0.33333333 Y=0.00000000 Z=0.33333333
ATOM -12: X=0.66666667 Y=0.00000000 Z=0.33333333
ATOM -13: X=0.00000000 Y=0.33333333 Z=0.33333333
ATOM -14: X=0.33333333 Y=0.33333333 Z=0.33333333
ATOM -15: X=0.66666667 Y=0.33333333 Z=0.33333333
ATOM -16: X=0.00000000 Y=0.66666667 Z=0.33333333
ATOM -17: X=0.33333333 Y=0.66666667 Z=0.33333333
ATOM -18: X=0.66666667 Y=0.66666667 Z=0.33333333
ATOM -19: X=0.00000000 Y=0.00000000 Z=0.66666667
ATOM -20: X=0.33333333 Y=0.00000000 Z=0.66666667
ATOM -21: X=0.66666667 Y=0.00000000 Z=0.66666667
ATOM -22: X=0.00000000 Y=0.33333333 Z=0.66666667
ATOM -23: X=0.33333333 Y=0.33333333 Z=0.66666667
ATOM -24: X=0.66666667 Y=0.33333333 Z=0.66666667
ATOM -25: X=0.00000000 Y=0.66666667 Z=0.66666667
ATOM -26: X=0.33333333 Y=0.66666667 Z=0.66666667
ATOM -27: X=0.66666667 Y=0.66666667 Z=0.66666667
ATOM -28: X=0.16666667 Y=0.16666667 Z=0.16666667
ATOM -29: X=0.50000000 Y=0.16666667 Z=0.16666667
ATOM -30: X=0.83333333 Y=0.16666667 Z=0.16666667
ATOM -31: X=0.16666667 Y=0.50000000 Z=0.16666667
ATOM -32: X=0.50000000 Y=0.50000000 Z=0.16666667
ATOM -33: X=0.83333333 Y=0.50000000 Z=0.16666667
ATOM -34: X=0.16666667 Y=0.83333333 Z=0.16666667
ATOM -35: X=0.50000000 Y=0.83333333 Z=0.16666667
ATOM -36: X=0.83333333 Y=0.83333333 Z=0.16666667
ATOM -37: X=0.16666667 Y=0.16666667 Z=0.50000000
ATOM -38: X=0.50000000 Y=0.16666667 Z=0.50000000
ATOM -39: X=0.83333333 Y=0.16666667 Z=0.50000000
ATOM -40: X=0.16666667 Y=0.50000000 Z=0.50000000
ATOM -41: X=0.50000000 Y=0.50000000 Z=0.50000000
ATOM -42: X=0.83333333 Y=0.50000000 Z=0.50000000
ATOM -43: X=0.16666667 Y=0.83333333 Z=0.50000000
ATOM -44: X=0.50000000 Y=0.83333333 Z=0.50000000
ATOM -45: X=0.83333333 Y=0.83333333 Z=0.50000000
ATOM -46: X=0.16666667 Y=0.16666667 Z=0.83333333
ATOM -47: X=0.50000000 Y=0.16666667 Z=0.83333333
ATOM -48: X=0.83333333 Y=0.16666667 Z=0.83333333
ATOM -49: X=0.16666667 Y=0.50000000 Z=0.83333333
ATOM -50: X=0.50000000 Y=0.50000000 Z=0.83333333
ATOM -51: X=0.83333333 Y=0.50000000 Z=0.83333333
ATOM -52: X=0.16666667 Y=0.83333333 Z=0.83333333
ATOM -53: X=0.50000000 Y=0.83333333 Z=0.83333333
ATOM -54: X=0.83333333 Y=0.83333333 Z=0.83333333
ATOM -55: X=0.41666667 Y=0.50000000 Z=0.33333333\
"

# Parse ideal impurity position:
ideal_impurity_line=$(echo "$ideal_crds" | grep "${impurity_id}:")


#---> Print useful information:
echo "\
Lattice constant: $alat
Impurity atom   : $impurity, $impurity_id
Number of atoms : $atoms_num
"

#---> Main part - calculate shift:
unset list list_4_print
for ((i=1; i<=$atoms_num; i++)); do
    unset ideal_x ideal_y ideal_z ideal_line
    unset current_x current_y current_z current_line
    unset distance_from_impurity_ideal distance_from_impurity
    unset atom_shift

    # Ideal structure processing:
    ideal_line=$(echo "$ideal_crds" | head -$i | tail -1)

    # Calculate distance from impurity position to Fe atom in ideal structure:
    calc_distance "$ideal_line" "$ideal_impurity_line"; distance_from_impurity_ideal=$distance


    # Real structure processing:
    # Find current line of crds, parse an atom crds, move the coordinate to the initial unit cell.  
    current_line=$(echo "$current_crds" | head -$i | tail -1)

    # Calculate distance from impurity to Fe atom in real structure:
    calc_distance "$current_line" "$impurity_line"; distance_from_impurity=$distance

    # Calculate shift of Fe atoms from ideal positions:
    atom_shift=$(echo "scale=12; $distance_from_impurity - $distance_from_impurity_ideal" | bc)
    
    # Organizing printable version of the distances and shifts:
    distance_from_impurity=$(printf "%12s" "$(printf "%10.8f\n" $distance_from_impurity)")
    distance_from_impurity_ideal=$(printf "%12s" "$(printf "%10.8f\n" $distance_from_impurity_ideal)")
    atom_shift=$(printf "%15s" "$(printf "%10.8f\n" $atom_shift)")


    # Save data in variables:
    list="$list
${i}\t${atom_shift}\t${distance_from_impurity}\t${distance_from_impurity_ideal}"

    list_4_print="${list_4_print}
${distance_from_impurity}\t\
${distance_from_impurity_ideal}\t\
${atom_shift}"

done

#echo -e "$list" | sort -nk3
list_4_print=$(echo -e "${list_4_print}" | sort -nk1)
echo -e "$list_4_print"


#---> H-related information:
# H spheres:
H_1st="ATOM -55: X=0.41666667 Y=0.50000000 Z=0.33333333"
H_2nd="ATOM -55: X=0.08333333 Y=0.50000000 Z=0.33333333"
H_3rd="ATOM -55: X=0.41666667 Y=0.50000000 Z=0.66666667"
H_4th="ATOM -55: X=0.08333333 Y=0.50000000 Z=0.66666667"

calc_distance "$H_1st" "$ideal_impurity_line"; distance_from_impurity_to_H1=$(printf "%10.8f\n" $distance)
calc_distance "$H_2nd" "$ideal_impurity_line"; distance_from_impurity_to_H2=$(printf "%10.8f\n" $distance)
calc_distance "$H_3rd" "$ideal_impurity_line"; distance_from_impurity_to_H3=$(printf "%10.8f\n" $distance)
calc_distance "$H_4th" "$ideal_impurity_line"; distance_from_impurity_to_H4=$(printf "%10.8f\n" $distance)

echo -e "\n\
Distance from $impurity to H (1st sphere): $distance_from_impurity_to_H1
Distance from $impurity to H (2nd sphere): $distance_from_impurity_to_H2
Distance from $impurity to H (3rd sphere): $distance_from_impurity_to_H3
Distance from $impurity to H (4th sphere): $distance_from_impurity_to_H4
"


exit 0

