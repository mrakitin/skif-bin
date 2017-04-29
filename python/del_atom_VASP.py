#!/usr/bin/python

import os, sys
import glob


def del_atom(poscar, atom, debug=False):
    ''' The function removes specified element(s) from the POSCAR.'''
    
    out_poscar = None
    
    if os.path.exists(poscar):
        with open(poscar, 'rb') as f:
            content = f.readlines()

        # Find number of atoms to remove:
        atoms_list   = content[5].split()
        numbers_list = content[6].split()
        atom_order   = atoms_list.index(atom)
        total_atoms  = len(atoms_list)

        new_names = atoms_list[:]
        del new_names[atom_order]

        new_numbers = numbers_list[:]
        del new_numbers[atom_order]

        count = 0
        for i in range(atom_order):
            count += int(numbers_list[i])

        start_row = 8    # coordinates start at this row in POSCAR

        skip_rows    = start_row + count - 1
        remove_start = skip_rows + 1
        remove_end   = remove_start + int(numbers_list[atom_order]) - 1

        out_poscar_tmp1 = poscar.split('_')[0]
        out_poscar_tmp2 = poscar.split('_')[1]
        out_poscar_tmp1 = out_poscar_tmp1.replace(atom, '').replace(numbers_list[atom_order], '')
        out_poscar = out_poscar_tmp1 + '_' + out_poscar_tmp2

        # Write a new POSCAR:
        out = ''
        for i in range(len(content)):
            if i == 0:
                tmp = content[i].split()
                tmp1 = tmp[0]
                tmp2 = content[i].replace(tmp1, '')
                tmp1 = tmp1.replace(atom, '').replace(numbers_list[atom_order], '')
                out += tmp1 + tmp2
            elif i == 5:
                out += ' '.join(new_names) + '\n'
            elif i == 6:
                out += ' '.join(new_numbers) + '\n'
            elif i < remove_start or i > remove_end:
                out += content[i]

        with open(out_poscar, 'wb') as f:
            f.write(out)

        if debug:
            print 'Atom %s order: %i of %i' % (atom, atom_order+1, total_atoms)
            print 'Old names:', atoms_list,   'New names:', new_names
            print 'Old nums :', numbers_list, 'New nums :', new_numbers
            print 'Number of atoms to pass: %5i' % (count)
            print 'Skip rows              : %5i' % (skip_rows)
            print 'The following rows will be removed: %i ... %i\n' % (remove_start, remove_end)
    
    return out_poscar



#print del_atom('Fe54H_8.53746040.vasp', 'H')
#print del_atom('Fe54H_8.53746040.vasp', 'Fe')
for f in glob.glob('Fe54H_*'):
    if os.path.isfile(f):
        print del_atom(f, 'H')
        print del_atom(f, 'Fe')
