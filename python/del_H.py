#!/usr/bin/python

'''
Description:

    The script is a part of the procedure to obtain charge density difference plots.
    More details about the procedure:
	- http://vaspnotes.blogspot.com/2013/10/charge-density-difference-plots.html;
        - http://renqinzhang.weebly.com/uploads/9/6/1/9/9619514/charge_density_difference.pdf;
        - http://www.nims.go.jp/cmsc/staff/arai/wien/venus.html.

    Related files: ~/bin/skif-bin/python/del_Fe53Me.py
                   ~/bin/skif-bin/python/calc_prepare.sh

    The script is to remove H atom from the Fe53MeH.struct relaxed file.
    53 Fe and 1 Me atoms will remain in the system with the same lattice 
    parameters and positions of atoms.

Date  : 2015-01-27
Author: Maxim Rakitin (maxim.rakitin@gmail.com)

'''

import os, sys

if len(sys.argv) <= 2:
    print 'Specify input and output files as first and second arguments.'
    sys.exit(1)

infile  = sys.argv[1]
outfile = sys.argv[2]

if not os.path.exists(infile):
    print 'File %s does not exist. Exit.' % infile
    sys.exit(1)

with open(infile, 'rb') as f:
    content = f.readlines()

content[0] = content[0].replace('H', '')
content[1] = content[1].replace('55', '54')

for i in range(len(content)):
    if content[i].find('ATOM') >= 0 and content[i].find('55:') >= 0:
	start = i
	end   = start + 5
	break

print'\nRemove lines from %i to %i...' % (start, end)

with open(outfile, 'wb') as f:
    for i in range(len(content)):
        if i >= start and i <= end:
	    continue
        f.write(content[i])

print 'Done.\n'
