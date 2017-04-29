#!/usr/bin/python

import os, sys

if len(sys.argv) > 1:
    struct_file = sys.argv[1]
    print '\nYou are about to convert %s to VASP POSCAR file.' % (struct_file)
else:
    print 'Please specify WIEN2k .struct file to convert.'
    sys.exit(1)

if not os.path.exists(struct_file):
    print 'Specified file %s does not exist. Exit.\n' % struct_file
    sys.exit(2)
    

poscar_file = struct_file.split('.')[0] + '.vasp'

f = open(struct_file, 'rb')
struct_content = f.readlines()
f.close()


def alat2mat(alat):
    mat = []
    mat.append([alat[0], 0,       0    ])
    mat.append([0,       alat[1], 0    ])
    mat.append([0,       0,       alat[2]])

    return mat

def mat2print(mat):
    text = ''
    for i in range(len(mat)):
	tmp = '%12.8f %12.8f %12.8f' % (mat[i][0], mat[i][1], mat[i][2])
	text += tmp + '\n'
    return text

sys_name = struct_content[0].strip()	# First row in the file
alat     = []
alat_num = []
atoms    = []
coords   = []

# alat (4th row in the file):
alat = struct_content[3].split()
for i in range(len(alat)):
    # Since WIEN2k values are in a.u. (Bohr radii), but in VAPS they are in A (Angstroms),
    # we need to convert the values here:
    alat_num.append(float(alat[i])*0.529177)


for i, row in enumerate(struct_content):
    atom  = ''
    coord = ''
    x = ''
    y = ''
    z = ''
    
    
    if row.find('Z:') >= 0:
	atom = row.split()[0]
	atoms.append(atom)

    if row.find('ATOM') >= 0 and row.find('ATOMS') < 0:
	coord_tmp = row
	x = float(coord_tmp.split('X=')[1].split()[0])
	y = float(coord_tmp.split('Y=')[1].split()[0])
	z = float(coord_tmp.split('Z=')[1].split()[0])

	coord = [x, y, z]
	
	coords.append(coord)

print ''
print '\tSystem name           : %s'   % sys_name
print '\tLattice parameters    : %s'   % ' '.join(alat)
print '\tNumber of found atoms : %i'   % len(atoms)
print '\tNumber of found coords: %i\n' % len(coords)

# Convert text to float matrix:
alat_mat = alat2mat(alat_num)
#print mat2print(alat_mat)

'''
if len(atoms) == len(coords):
    for i in range(len(coords)):
	print '%-10s %s' % (atoms[i], '  '.join(coords[i]))
print ''
'''


uniq_atoms = []
for atom in atoms:
    if atom not in uniq_atoms:
	uniq_atoms.append(atom)

uniq_atoms.sort()
#print '' uniq_atoms

counter = []
for i, atom in enumerate(uniq_atoms):
    counter.append(0)
    for j in range(len(atoms)):
	if atoms[j] == atom:
	    #print '%10i, %10s' % (j, atom)
	    counter[i] += 1
    counter[i] = str(counter[i])

coords_str = ''
for i, atom in enumerate(uniq_atoms):
    for j in range(len(coords)):
	if atoms[j] == atom:
	    tmp = '%12.8f %12.8f %12.8f' % (coords[j][0], coords[j][1], coords[j][2])
	    coords_str += tmp + '\n'


# Create the content of POSCAR file:
poscar_content = ''
poscar_content += sys_name + '\n'
poscar_content += '1.0000' + '\n'
poscar_content += mat2print(alat_mat)
poscar_content += ' '.join(uniq_atoms) + '\n'
poscar_content += ' '.join(counter) + '\n'
poscar_content += 'Direct' + '\n'
poscar_content += coords_str

print '\n\n' + poscar_content

# Write data to a file in VASP POSCAR format:
f = open(poscar_file, 'wb')
f.write(poscar_content)
f.close()















