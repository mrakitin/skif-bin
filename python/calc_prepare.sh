#!/bin/bash

# Description:
#
#    The script is a part of the procedure to obtain charge density difference plots.
#    More details about the procedure:
#	- http://vaspnotes.blogspot.com/2013/10/charge-density-difference-plots.html;
#        - http://renqinzhang.weebly.com/uploads/9/6/1/9/9619514/charge_density_difference.pdf;
#        - http://www.nims.go.jp/cmsc/staff/arai/wien/venus.html.
#
#    Related files: ~/bin/skif-bin/python/del_H.py
#                   ~/bin/skif-bin/python/del_Fe53Me.py
#
#    The script fully prepares calculation folder and .struct file from relaxed Fe53MeH.struct.
#
# Date  : 2015-01-27
# Author: Maxim Rakitin (maxim.rakitin@gmail.com)


idir=$PWD

#---> Prepare Fe53Me:
for i in Fe53*H*; do
    echo $i
    name=$(echo $i | sed 's/H//g')
    echo $name
    mkdir -v $name
    cp -v $i/$i.struct $name/
    cd $name
    #ls -alF
    python ~/bin/skif-bin/python/del_H.py $i.struct ${name}.struct
    nohup init_lapw -red 0 -vxc 13 -ecut -7.0 -rkmax 10.0 -numk 24 -b -sp -nosgroup >> init.log 2>> init.err &
    sjob -n 1:1-0 -s runsp -lapw0 para
    cd $idir
    echo -e '\n\n'
done


#---> Prepare H:
for i in Fe53*H*; do
    echo $i
    name=$(echo $i | sed 's/'"$(echo $i | sed 's/H//g' | cut -d_ -f1)"'//')
    echo $name
    mkdir -v $name
    cp -v $i/$i.struct $name/
    cd $name
    #ls -alF
    python ~/bin/skif-bin/python/del_Fe53Me.py $i.struct ${name}.struct
    nohup init_lapw -red 0 -vxc 13 -ecut -7.0 -rkmax 3.5 -numk 24 -b -sp -nosgroup >> init.log 2>> init.err &
    sjob -n 1:1-0 -s runsp -lapw0 para
    cd $idir
    echo -e '\n\n'
done

