#!/usr/bin/env python

import sys, os
import re
from optparse import OptionParser

DEBUG = 0
TESTRUN = 0
PROFILE = 0

def au2ang(au_coordinates, lattice_parameter, type):
    au2ang = 0.529177
    if type == 'bulk':
        coordinate_limit = 0.98
    if type == 'grain':
        coordinate_limit = 0.99
    ang_coordinates = []
    for coordinate in au_coordinates:
        if coordinate < coordinate_limit:
            ang_coordinates.append(coordinate * lattice_parameter * au2ang)
        else:
            ang_coordinates.append((1 - coordinate) * lattice_parameter * au2ang)
    return ang_coordinates

def format_print (float_num):
    round_num = '%.3f' %float_num
    num_lenght = len(round_num)
    diff_lenght = 8 - num_lenght
    if diff_lenght > 0:
        format_num = round_num
        for i in xrange(diff_lenght):
            format_num = ' ' + format_num
    else:
        format_num = None
    return format_num

def main(argv=None):

    program_name = os.path.basename(sys.argv[0])

    try:
        # setup option parser
        parser = OptionParser()
        parser.add_option("-n", "--name", dest="name", default="Not defined", help="set struct/scf file base name or folder name where required files are located")
        parser.add_option("-t", "--type", dest="type", help="set configuration type: grain or bulk")

        (options, args) = parser.parse_args()
        parser.destroy()

        if not options.type:
            print "Configuration type (grain/bulk) is not specified!"
            sys.exit()

        if options.name == 'Not defined':
            run_dir = os.getcwd()
            case_name = os.path.basename(run_dir)
        else:
            run_dir = os.path.dirname(os.path.abspath(options.name))
            case_name = os.path.basename(options.name)

        struct_file_name = run_dir + '/' + case_name + '.struct'
        scf_file_name = run_dir + '/' + case_name + '.scf'
        if not os.path.exists(struct_file_name) or not os.path.exists(scf_file_name):
                print "STRUCT and/or SCF files not found! Please set correct file base name or folder. Exiting..."
                sys.exit()

        # MAIN BODY #

        #-------------------------------------------------------------
        #sopostavlenie charges and atom names
        atom_dict = {
                     '26': {
                            'atom' : 'Fe',
                            'color': {
                                      'up'  : '[0,0,255]',
                                      'down': '[255,0,0]'
                                      }
                            },
                     '6' : {
                            'atom' : 'C',
                            'color': {
                                      'up'  : '[0,255,0]',
                                      'down': '[0,255,0]'
                                      }
                            },
            }

        #-------------------------------------------------------------
        rsm_file_name = run_dir + '/' + case_name + '.rsm'
        rsm_head = '''REMARK  atoms as in       Fe54H.pdb\nREMARK< i5><  > X     <  >    <x f8.3><y f8.3><z f8.3><f6.2><f6.3>\n'''
        rsm_middle = '''
#!rasmol -rsm file
# Creator: RasTop Version 2.1.0
zap
set connect on
load pdb inline
set title Fe53_vac

# Colour details
background [0,0,0]
set backfade off
set headlight [-79,17,-58]
set ambient 40
set specular on
set specpower 30
set shadepower 50
set depthcue off
set shadow off
stereo off

# Transformation
reset
rotate molecule
set picking ident
set worlddepth 6028
# zoom 100.00
scale 24.11
position x 0.000 y -0.000 z -0.000

# Rendering
colour axes [255,255,255]
set axes off
set boundingbox on
set unitcell off
set bondmode and
dots off

# Avoid Colour Problems!
select all
colour bonds none
colour backbone none
colour hbonds none
colour ssbonds none
colour ribbons none
colour white
'''
        rsm_end = '''
select all
spacefill 50
set shadow off

# Bonds
wireframe off

# Ribbons
ribbons off

# Backbone
backbone off

# Labels
labels off

# Monitors
monitors off

# ssbonds
ssbonds off

# hbonds
hbonds off

# Dots
set solvent false
set radius 0
set dots 1
dots off

# AtomSets
# no sets

select all

# World Transformation
rotate world
centre origin
set axes world on
colour world axes [255,255,255]
# translate world x -4.15
position world x -1.000 y -0.000
reset slab
slab off
reset depth
depth off
centre origin
molecule 1

exit'''
        #-------------------------------------------------------------
        struct_file = open(struct_file_name,'rb')
        struct_data = struct_file.read()
        struct_file.close()

        scf_file = open(scf_file_name,'rb')
        scf_data=scf_file.read()
        scf_file.close()
        #-------------------------------------------------------------

        # find lattice parameters 
        struct_lines = struct_data.split('\n')

        for i,line in enumerate(struct_lines):
            item = line.find('ATOM  -1')
            if item >= 0:
                header_position = i - 1
                break
        pattern_coordinates = '[\d]{1,9}.[\d]{1,9}'
        reg_coordinates = re.compile(pattern_coordinates)
        parameters = re.findall(reg_coordinates, struct_lines[header_position])
        a = float(parameters[0])
        b = float(parameters[1])
        c = float(parameters[2])
        #------------------------------------------------------------

        # creation of patterns for regular expressions 
        pattern_X = 'X=0.[\d]{0,8}'
        pattern_Y = 'Y=0.[\d]{0,8}'
        pattern_Z = 'Z=0.[\d]{0,8}'
        pattern_charge = 'Z:[\s]{1,3}[\d]{0,3}'
        pattern_moment = 'MAGNETIC MOMENT IN SPHERE[\s]{1,3}[\d]{0,3}[\s]{4}=[\s]{3,4}[-\d]{0,9}.[\d]{0,9}'

        reg_X = re.compile(pattern_X)
        reg_Y = re.compile(pattern_Y)
        reg_Z = re.compile(pattern_Z)
        reg_charge = re.compile(pattern_charge)
        reg_moment = re.compile(pattern_moment)

        # find XYZ coordinations and atom names using  regular expressions
        X = re.findall(reg_X,struct_data)
        X = [float(i.split('=')[1]) for i in X]
        Y = re.findall(reg_Y,struct_data)
        Y = [float(i.split('=')[1]) for i in Y]
        Z = re.findall(reg_Z,struct_data)
        Z = [float(i.split('=')[1]) for i in Z]
        charges = re.findall(reg_charge, struct_data)
        charges = [i.split(':')[1].strip() for i in charges]

        number_of_atoms = len(X)

        moments = re.findall(reg_moment,scf_data)
        moments = [float(i.split('=')[1].strip()) for i in moments[-1 * number_of_atoms:]]

        X_ang = au2ang(X, a, options.type)
        Y_ang = au2ang(Y, b, options.type)
        Z_ang = au2ang(Z, c, options.type)

        for i in xrange(len(X)):
            print 'X:', X_ang[i], 'Y:', Y_ang[i], 'Z:', Z_ang[i], 'atom:', atom_dict[charges[i]]['atom'], 'moment:', moments[i]

        rsm_atoms  = []
        rsm_colors = ['#Atoms\n']

        for i, (x, y, z) in enumerate(zip(X_ang, Y_ang, Z_ang)):
            atom_line = "ATOM   %3d"%(i + 1) + "  IS%3d"%(i + 1) + "       1     " + format_print(x) + format_print(y) +  format_print(z) + " 0.000 0.001\n"
            rsm_atoms.append(atom_line)

        for i, (charge, moment) in enumerate(zip(charges, moments)):
            if moment > 0:
                color_flag = 'up'
            else:
                color_flag = 'down'
            color_line = "select atomno=" + str(i + 1) + "\ncolour atoms" + atom_dict[charge]['color'][color_flag] + "\n"
            rsm_colors.append(color_line)
        #-----------------------------------------------------------------
        #-----------------------------------------------------------------
        rsm_file = open(rsm_file_name, 'wb')
        rsm_file.write(rsm_head)
        rsm_file.writelines(rsm_atoms)
        rsm_file.write(rsm_middle)
        rsm_file.writelines(rsm_colors)
        rsm_file.write(rsm_end)
        rsm_file.close()

    except Exception, e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'soap_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
