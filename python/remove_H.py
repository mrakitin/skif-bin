'''
Created on 20.04.2013

@author: Maxim
'''

import sys, os
from optparse import OptionParser

#-------------------------------------------------------------------------------
parser = OptionParser()
parser.add_option("-s", "--struct", dest="struct",
                  help="Specify WIEN2k struct file", metavar="FILE")
(options, args) = parser.parse_args()

if not options.struct:
    parser.error('No struct file specified.')

parser.destroy()
#-------------------------------------------------------------------------------

struct_file     = os.path.abspath(options.struct)
new_struct_file = os.path.basename(struct_file).replace('H','')
print 'WIEN2k struct file with H   :', struct_file
print 'WIEN2k struct file without H:', new_struct_file
print

filein = open(struct_file, 'rb')
file_content = filein.readlines()
filein.close


atoms_num  = int(file_content[1].split()[-1])
new_atoms_num = atoms_num - 1
print 'Atoms number      :', atoms_num
print 'New atoms number  :', new_atoms_num
print

lines_num = len(file_content) 
print 'Total lines number:', lines_num

H_line_num    = -1
H_block_start = -1
H_block_end   = -1
for i in xrange(lines_num):
    if file_content[i].find('H') == 0:
        H_line_num = i
        #print 'i = ' + str(i) + ':', file_content[i]
        break

'''
ATOM -55: X=0.41201749 Y=0.49997971 Z=0.33334069
          MULT= 1          ISPLIT= 2
H          NPT=  781  R0=0.00010000 RMT=    0.7000   Z:   1.00000
LOCAL ROT MATRIX:    1.0000000 0.0000000 0.0000000
                     0.0000000 1.0000000 0.0000000
                     0.0000000 0.0000000 1.0000000
'''

if H_line_num >= 0:
    H_block_start = i - 2
    H_block_end = i + 3

print 'H atom line number:', H_line_num
print 'H block start     :', H_block_start
print 'H block end       :', H_block_end

fileout = open(new_struct_file, 'wb')
for i in xrange(lines_num):
    if i == 1:
        file_content[i] = file_content[i].replace(str(atoms_num), str(new_atoms_num))
    if i < H_block_start or i > H_block_end:
        #print file_content[i]
        fileout.write(file_content[i])
fileout.close()
