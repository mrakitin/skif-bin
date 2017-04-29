#!/usr/bin/python

'''
Description:

    The script is a part of the procedure to obtain charge density difference plots.
    More details about the procedure:
	- http://vaspnotes.blogspot.com/2013/10/charge-density-difference-plots.html;
        - http://renqinzhang.weebly.com/uploads/9/6/1/9/9619514/charge_density_difference.pdf;
        - http://www.nims.go.jp/cmsc/staff/arai/wien/venus.html.

    Related files: ~/bin/skif-bin/python/del_H.py
                   ~/bin/skif-bin/python/calc_prepare.sh

    The script is to remove Fe53Me atoms from the Fe53MeH.struct relaxed file.
    Only one H atom with number 55 will remain in the system with the same
    lattice parameters and position of H. WIEN2k will complain if there is one
    H atom placed not to the beginning of the coordinates. So one more H atom
    is placed to the beginning of the coordinates (0, 0, 0). This should not
    affect the resulted density.

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

content[0] = content[0].replace(content[0].strip(), outfile.replace('.struct', ''))
content[1] = content[1].replace('55', ' 2')

for i in range(len(content)):
    if content[i].find('ATOM') >= 0 and content[i].find('55:') >= 0:
	content[i] = content[i].replace('ATOM -55:', 'ATOM  -2:')
	start = i
	end   = len(content) - 1
	break

# Header part we need to leave:
head_start = 0
head_end   = 3

print'\nLeave lines from %i to %i...' % (head_start, head_end)
print'\nLeave lines from %i to %i...' % (start, end)

with open(outfile, 'wb') as f:
    for i in range(head_start, head_end + 1):
        f.write(content[i])

    artificial_atom = '''\
ATOM  -1: X=0.00000000 Y=0.00000000 Z=0.00000000
          MULT= 1          ISPLIT= 2
H          NPT=  781  R0=0.00010000 RMT=    0.7000   Z:   1.00000
LOCAL ROT MATRIX:    1.0000000 0.0000000 0.0000000
                     0.0000000 1.0000000 0.0000000
                     0.0000000 0.0000000 1.0000000
'''
    f.write(artificial_atom)

    for i in range(start, end + 1):
        f.write(content[i])


print 'Done.\n'
