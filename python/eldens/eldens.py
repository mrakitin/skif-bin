#!/usr/bin/python
# encoding: utf-8

# Description: the code it to parse case.rho file with electronic density values
#              and calculate charge in the parallelepiped cell from {0; 0; 0} to
#              {1; 1; 1} around hydrogen atom.
# Author     : Maxim Rakitin
# Date       : 2013-10-03 22:47
#              2013-11-24 22:53
#              2013-12-23 23:00

import os, sys
from optparse import OptionParser
from time import localtime, strftime


#-------------------------------- Options --------------------------------------
parser = OptionParser()
parser.add_option("-n", "--case_name", dest="case_name",
                  help="Specify CASE name", metavar="CASE")
parser.add_option("-x", "--x_steps", dest="x_steps",
                  help="Specify number of X steps", metavar="NUM")
parser.add_option("-y", "--y_steps", dest="y_steps",
                  help="Specify number of Y steps", metavar="NUM")
parser.add_option("-z", "--z_steps", dest="z_steps",
                  help="Specify number of Z steps", metavar="NUM")

(options, args) = parser.parse_args()

if not options.case_name:
    parser.error('Case name not specified.')

if options.x_steps:
    x_steps = int(options.x_steps)
else:
    x_steps = 100   # Default value
if options.y_steps:
    y_steps = int(options.y_steps)
else:
    y_steps = 100   # Default value
if options.z_steps:
    z_steps = int(options.z_steps)
else:
    z_steps = 100   # Default value

parser.destroy()
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Initialize values:
case_name   = options.case_name   # 'Fe54'
struct_file = case_name + '.struct'
in5_file    = case_name + '.in5c'
rho_file    = case_name + '.rho'
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Generate case.in5c file using coordinates of Fe atoms from the case.struct file:
# atoms_nums = [14, 17, 32, 41]

f = open(struct_file, 'rb')
struct_content = f.readlines()
f.close()

alats_split = struct_content[3].split()
alats = []
for i in xrange(3):
    alats.append(float(alats_split[i]))
#print 'alats:', alats

atom14_crd = []
atom17_crd = []
atom32_crd = []
atom41_crd = []

for i, value in enumerate(struct_content):
    # Atom 14:
    if value.find('ATOM ') >= 0 and value.find('-14:') >= 0:
        atom14_split = value.split(':')[1].split()
        for i in atom14_split:
            atom14_crd.append(float(i.split('=')[1]))

    # Atom 17:
    if value.find('ATOM ') >= 0 and value.find('-17:') >= 0:
        atom17_split = value.split(':')[1].split()
        for i in atom17_split:
            atom17_crd.append(float(i.split('=')[1]))

    # Atom 32:
    if value.find('ATOM ') >= 0 and value.find('-32:') >= 0:
        atom32_split = value.split(':')[1].split()
        for i in atom32_split:
            atom32_crd.append(float(i.split('=')[1]))

    # Atom 41:
    if value.find('ATOM ') >= 0 and value.find('-41:') >= 0:
        atom41_split = value.split(':')[1].split()
        for i in atom41_split:
            atom41_crd.append(float(i.split('=')[1]))
    #---------------------------------------------------------------------------

begin_crd  = [0.00000000, 0.00000000, 0.00000000]
end_crd    = [1.00000000, 1.00000000, 1.00000000]

divider = 100000000

#all_x_crds = [atom14_crd[0], atom17_crd[0], atom32_crd[0], atom41_crd[0]]
all_x_crds = [begin_crd[0], end_crd[0]]

all_x_crds.sort()
x_min = all_x_crds[0]
x_max = all_x_crds[-1]
x_min_in5 = int(x_min * divider)
x_max_in5 = int(x_max * divider)


#all_y_crds = [atom14_crd[1], atom17_crd[1], atom32_crd[1], atom41_crd[1]]
all_y_crds = [begin_crd[1], end_crd[1]]

all_y_crds.sort()
y_min = all_y_crds[0]
y_max = all_y_crds[-1]
y_min_in5 = int(y_min * divider)
y_max_in5 = int(y_max * divider)


#all_z_crds = [atom14_crd[2], atom17_crd[2], atom32_crd[2], atom41_crd[2]]
all_z_crds = [begin_crd[2], end_crd[2]]

all_z_crds.sort()
z_min = all_z_crds[0]
z_max = all_z_crds[-1]
z_min_in5 = int(z_min * divider)
z_max_in5 = int(z_max * divider)

z_increment = (z_max_in5 - z_min_in5)/z_steps

for z_i in xrange(z_steps + 1):
    
    z_current = z_min_in5 + z_increment * z_i
    print '\nStatus: {0:.2f}% completed...'.format(float(z_current)/float(z_max_in5 - z_min_in5)*100.0)
    
    '''
    print 'z_min_in5:', z_min_in5
    print 'z_max_in5:', z_max_in5
    '''
    
    in5_content = '''\
    ''' + str(x_min_in5) + '''    ''' + str(y_min_in5) + '''    ''' + str(z_current) + '''      ''' + str(divider) + '''
    ''' + str(x_max_in5) + '''    ''' + str(y_min_in5) + '''    ''' + str(z_current) + '''      ''' + str(divider) + '''
    ''' + str(x_min_in5) + '''    ''' + str(y_max_in5) + '''    ''' + str(z_current) + '''      ''' + str(divider) + '''
3 3 3
''' + str(x_steps) + ' ' + str(y_steps) + '''
RHO ADD
ATU TOT NODEBUG
NONORTHO
'''
    
    #print 'in5_content:\n', in5_content
    f = open(in5_file, 'wb')
    f.writelines(in5_content)
    f.close()
    #---------------------------------------------------------------------------
    
    
    #---------------------------------------------------------------------------
    # Run lapw5 -c -up/-dn with generated case.in5c file:
    for spin in ['up']:
        print '\tRunning "x lapw5 -c -' + spin + '" command...'
        os.popen('x lapw5 -c -' + spin)
    
        #---------------------------------------------------------------------------
        # Read and process the content of the case.rho file:
        f = open(rho_file, 'rb')
        rho_content = f.readlines()
        f.close()
        
        cols_num = 5
        parms_dict = rho_content[0].split()
        #print parms_dict
        x_points = int(parms_dict[0])
        y_points = int(parms_dict[1])
        x_length = float(parms_dict[2])
        y_length = float(parms_dict[3])
        
        #print 'x_points:', x_points
        #print 'y_points:', y_points
        print '\tcase.rho processing...'
        #print 'x_length:', x_length
        #print 'y_length:', y_length
        
        rows_num = len(rho_content)
        #print 'rows_num:', rows_num
        
        one_dim_points    = []
        second_dim_points = []
        for i in xrange(1, rows_num):
            row_values = rho_content[i].split()
            row_values = map(float, row_values)
            if len(one_dim_points) < x_points:
                one_dim_points += row_values
            elif len(one_dim_points) == x_points:
                second_dim_points.append(one_dim_points)
                one_dim_points = row_values
        second_dim_points.append(one_dim_points)
        
        outfile = rho_file + '.out_' + spin
        f = open(outfile, 'wb')
        for i, values in enumerate(second_dim_points):
            y = float(i) * y_length / float(y_points - 1)
            for j in xrange(len(values)):
                x = float(j) * x_length / float(x_points - 1)
                out_row = str(x) + ',' +  str(y) + ',' + str(values[j]) + '\n'
                #print out_row
                f.write(out_row)
        f.close()
        os.rename(rho_file, rho_file + '_'  + str(z_i).zfill(3) + '_' + spin)
        print '\tcase.rho processing finished.'
        
    os.rename(in5_file, in5_file + '_'  + str(z_i).zfill(3))
    os.popen('rm -f .running.*')


timestamp = strftime("%Y-%m-%d_%H-%M-%S", localtime())
rho_dir = 'rho_files_' + str(timestamp)
os.mkdir(rho_dir)
os.popen('mv -f ' + case_name +'.in5* ' + rho_dir)
os.popen('mv -f ' + case_name +'.rho_*_up ' + rho_dir)

print '\nEldens generation finished. Files saved in ' + rho_dir + ' directory.'
exit(0)
