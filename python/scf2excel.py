#!/usr/bin/env python

# Author : Maxim Rakitin (based on code of Galina Ruzanova)
# Date   : 2013-07-05 15:00
# Updated: 2013-08-04 14:35

import re
import os
import xlwt
import glob
from optparse import OptionParser

#-------------------------------------------------------------------------------
# Options processing:
parser = OptionParser()
parser.add_option("-i", "--impurity", dest="impurity",
                  help="Specify impurity atom name", metavar="IMPURITY")
#parser.add_option("-s", "--sphere", dest="sphere",
#                  help="Specify coordination sphere number (1-5)", metavar="SPHERE")
parser.add_option("-v", action="store_true", dest="verbose",
                  help="Specify verbose mode", metavar="VERBOSE")
(options, args) = parser.parse_args()

if not options.impurity:
    parser.error('No impurity atom specified.')

#if not options.sphere:
#    parser.error('No coordination sphere number specified.')

parser.destroy()
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
impurity = options.impurity
file_name = 'Fe53' + impurity + 'H_moments'
wb = xlwt.Workbook()

all_files_mask = 'Fe53' + impurity + 'H_0*.scf' 
path      = os.getcwd()
all_scf_files = glob.glob(path + '/' + all_files_mask)
spheres = []
for i in all_scf_files:
    sphere = os.path.basename(i).split('_')[1][1]
    if sphere not in spheres:
        spheres.append(sphere)
print 'Impurity:', impurity
print 'Spheres :', ' '.join(spheres)
print
for sphere in spheres:
    #---------------------------------------------------------------------------
    # Generate the dict with alats and calc_names:
    file_mask = 'Fe53' + impurity + 'H_0' + sphere + '*.scf' 
    
    path      = os.getcwd()
    scf_files = glob.glob(path + '/' + file_mask)
    
    scf_files.sort()
    
    alat_dict = {}
    alat_list = []
    for i in scf_files:
        i_basename = os.path.basename(i)
        case_name = '.'.join(i_basename.split('.')[0:-1])
        
        f = open(case_name + '.struct')
        struct_content = f.readlines()
        f.close()
    
        alat = float(struct_content[3].split()[1].strip())
        alat_dict[alat] = case_name
        alat_list.append(alat)

    alat_list.sort()
    alat_string = ''
    for i in alat_list:
        alat_string = alat_string + ' ' + str(i)
    print 'Sphere  :', sphere
    print 'Alats   :', alat_string.strip()
    
    f = open(path + '/' + alat_dict[alat_list[0]] + '.struct', 'rb')
    struct_list = f.readlines()
    f.close
    
    atom_name = []
    atom_Z    = []
    for i in struct_list:
        if i.find('Z:') >= 0:
            atom_name.append(i[0:10].strip())
            atom_Z.append(float(i.split()[-1].strip()))
    #---------------------------------------------------------------------------
    
    
    #---------------------------------------------------------------------------
    # Define styles of the columns:
    float_style = xlwt.XFStyle()
    float_style.num_format_str = '#,##0.000'
    
    float6_style = xlwt.XFStyle()
    float6_style.num_format_str = '##0.000000'
    
    int_style = xlwt.XFStyle()
    int_style.num_format_str = '#,##0'
    
    font0 = xlwt.Font()
    font0.bold = True
    
    alignment = xlwt.Alignment() # Create Alignment
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    
    hstyle = xlwt.XFStyle()
    hstyle.alignment = alignment
    hstyle.font = font0
    
    bold = xlwt.XFStyle()
    bold.font = font0
    
    int_style_bold = xlwt.XFStyle()
    int_style_bold.num_format_str = '#,##0'
    int_style_bold.font = font0
    
    float_style_bold = xlwt.XFStyle()
    float_style_bold.num_format_str = '#,##0.000'
    float_style_bold.font = font0
    
    center = xlwt.XFStyle()
    center.alignment = alignment
    #---------------------------------------------------------------------------
    
    
    #---------------------------------------------------------------------------
    # Prepare common part of worksheet:
    sheet_name = 'Fe53' + impurity + 'H_0' + sphere
    
    ws = wb.add_sheet(sheet_name)
    ws.write_merge(0, 1, 0, 1, sheet_name, hstyle)
    ws.write(2, 0, 'Atom number', hstyle)
    ws.write(2, 1, 'Atom name', hstyle)
    ws.write(2, 2, 'Atom Z', hstyle)
    
    ws.col(0).width = 3300
    ws.col(1).width = 3300
    ws.col(2).width = 4500
    
    ws.write(0, 2, 'Total Energy, Ry:', hstyle)
    ws.write(1, 2, 'Alat, a.u.:', hstyle)
    
    ws.write_merge(len(atom_name) + 5, len(atom_name) + 5, 0, 2, 'Total magnetic moment:')
    ws.write_merge(len(atom_name) + 6, len(atom_name) + 6, 0, 2, 'Interstitial magnetic moment:')
    
    impurity_row_num = ''
    for i in range(len(atom_name)):
        if atom_name[i] not in ['Fe', 'H']:
            ws.write(i + 3, 1, atom_name[i], hstyle)
            impurity_row_num = i
        else:
            ws.write(i + 3, 1, atom_name[i], center)
        
        if i == impurity_row_num:
            ws.write(i + 3, 0, i+1, bold)
            ws.write(i + 3, 2, atom_Z[i], int_style_bold)
        else:
            ws.write(i + 3, 0, i+1)
            ws.write(i + 3, 2, atom_Z[i], int_style)
    #---------------------------------------------------------------------------
            
    
    #---------------------------------------------------------------------------
    # Perform for all found structs:
    for num, alat in enumerate(alat_list):
        calc_name = alat_dict[alat]
    
        # Open case.scf and case.struct for reading:
        f = open(path + '/' + calc_name + '.scf', 'rb')
        data = f.read()
        scf_list = f.readlines()
        f.close()
    
        # Use regexp to find :ENE, :MMI, :MMII:
        patternE = r"TOTAL ENERGY IN Ry =     (.{15})"
        Enum= re.compile(patternE)
        E=Enum.findall(data)
        
        patternMMC = r"SPIN MAGNETIC MOMENT IN CELL   =   (.{8})"
        MMCnum= re.compile(patternMMC)
        MMC=MMCnum.findall(data) 
        
        patternMMII = r"MAGNETIC MOMENT IN INTERSTITIAL =   (.{8})"
        MMIInum= re.compile(patternMMII)
        MMII=MMIInum.findall(data)
        
        patternMMI = r"MAGNETIC MOMENT IN SPHERE(.{20})"
        MMInum= re.compile(patternMMI)
        MMI=MMInum.findall(data)
        
        for i in range(len(E)):
            E[i]=float(E[i])
            MMC[i]=float(MMC[i])
            MMII[i]=float(MMII[i])   
        Etot = E[-1]
        
        MMI1=[]
        for i in range(len(atom_name)):
            MMI1.append(float((MMI[-len(atom_name)+i]).split(None,3)[2]))
        
        
        ws.col(3 + num).width = 4500
        ws.write(0, 3 + num, Etot, float6_style)
        ws.write(1, 3 + num, alat, float6_style)
        ws.write(2, 3 + num, 'Magnetic moment', hstyle)
        
        for i in range(len(atom_name)):
            if i == impurity_row_num:
                ws.write(i + 3, 3 + num, MMI1[i], float_style_bold)
            else:
                ws.write(i + 3, 3 + num, MMI1[i], float_style)
        
        ws.write(len(atom_name) + 5, 3 + num, MMC[-1] , float_style)
        ws.write(len(atom_name) + 6, 3 + num, MMII[-1], float_style)
    print 'Generation of ' + sheet_name + ' completed.\n'
    #---------------------------------------------------------------------------
    
wb.save(path + '/' + file_name + '.xls')

print 'Generation completed!'
