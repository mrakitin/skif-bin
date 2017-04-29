
# coding: utf-8

# In[1]:

import os, sys
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt

# In[2]:

def find_forces(outcar, debug=False):

    if not os.path.exists(outcar):
        print 'No %s file found. Exit.' % (outcar)
        return None
    
    
    with open(outcar, 'rb') as f:
        content = f.readlines()

    forces_rows = []
    total_drift = []
    for i in range(len(content)):
        if content[i].find('TOTAL-FORCE') >= 0:
            forces_rows.append(i)
            if debug:
                print 'Row #: %i: %s' % (i, content[i])
        if content[i].find('total drift:') >= 0:
            total_drift.append(i)
            if debug:
                print 'Row #: %i: %s' % (i, content[i])

    if debug:
        print 'Last occurrence of "TOTAL-FORCE": %i' % (forces_rows[-1])
        print 'Last occurrence of "total drift": %i' % (total_drift[-1])
    
    atoms_num = total_drift[-1] - forces_rows[-1] - 2 - 1   # 2 rows with dashes as separator
    
    forces = np.zeros((atoms_num, 3))

    count = 0
    for i in range(forces_rows[-1] + 2, total_drift[-1]-1):
        forces_list = content[i].split()[3:]
        for j in range(0, 3):
            forces[count, j] = float(forces_list[j])
        count += 1

    if debug:
        print 'Atoms number:', atoms_num
        print 'Forces shape:', forces.shape

    data = []
    for i in range(forces.shape[0]):
        tot_force = np.sqrt( forces[i, 0]**2 + forces[i, 1]**2 + forces[i, 2]**2 )
        data.append(tot_force)
        if debug:
            print 'Total force on atom %' '2i: %10.6f' % (i+1, tot_force)

    if debug:
        print 'Max: %.4f eV/A, Std: %.4f eV/A' % (np.max(np.abs(data)), np.std(forces))
			
    # Plot part:
    fig = plt.figure(figsize=(16, 8))
    plt.rcParams.update({'font.size': 22})

    ax = fig.add_subplot(111)

    ax.set_title('Forces distribution, Max: %.4f, Std: %.4f' % (np.max(np.abs(data)), np.std(forces)) )
    ax.set_xlabel('# of atom')
    ax.set_ylabel('Force, eV/A')

    ax.set_xlim((0, forces.shape[0]-1))
    ax.axhline(0, color='black', linestyle='dotted')
    ax.grid()

    ax.plot(forces[:, 0], label='F$_{x}$: %.4f' % (np.std(forces[:,0])) )
    ax.plot(forces[:, 1], label='F$_{y}$: %.4f' % (np.std(forces[:,1])) )
    ax.plot(forces[:, 2], label='F$_{z}$: %.4f' % (np.std(forces[:,2])) )

    for i in [14, 17, 32, 41]:
        ax.axvline(i-1, color='c', linewidth=2)

    ax.legend(ncol=1, fontsize=16)

    fig.tight_layout()
    fig.savefig('forces_distribution.png', dpi=200)

    return np.max(np.abs(data))


# In[3]:

find_forces('OUTCAR', debug=True)


# In[3]:



