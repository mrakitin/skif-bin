#!/usr/bin/env python
import re
import os
import xlwt
from datetime import datetime

path=os.getcwd()
filename='/xyz2struct.struct'
data = file(path+filename).read()

file=open(path+filename,'r')
line=file.readlines()
del line[5]
a=(line[3].split())[0]
b=(line[3].split())[1]
c=(line[3].split())[2]
h=' %s  %s   %s  90.00000  90.00000  90.00000\n'%(a,b,c)
#b=(line[0].split())[0]
filen='/xyz.struct'


N=len(line)-9
f=open(path+filen,'w')
#f.tell()
f.write("Fe5.38_0.2_0.2\nP                           %i\n             RELA\n" %N)
f.write(h)
f.write("ATOM  -1: %s %s %s\n"%((line[4].split())[2],(line[4].split())[3],(line[4].split())[4]))
f.write("          MULT= 1          ISPLIT= 2\n")
f.write("Fe         NPT=  781  R0=0.00005000 RMT=    2.0000   Z:  26.00000\n")
f.write("LOCAL ROT MATRIX:    1.0000000 0.0000000 0.0000000\n")
f.write("                     0.0000000 1.0000000 0.0000000\n")
f.write("                     0.0000000 0.0000000 1.0000000\n")
for i in range(5,N+4):
   if i<=12:f.write("ATOM  -%i: %s %s %s\n"%(i-3,(line[i].split())[1],(line[i].split())[2],(line[i].split())[3]))
   else:f.write("ATOM -%i: %s %s %s\n"%(i-3,(line[i].split())[1],(line[i].split())[2],(line[i].split())[3]))
   f.write("          MULT= 1          ISPLIT= 2\n")
   f.write("Fe         NPT=  781  R0=0.00005000 RMT=    2.0000   Z:  26.00000\n")
   f.write("LOCAL ROT MATRIX:    1.0000000 0.0000000 0.0000000\n")
   f.write("                     0.0000000 1.0000000 0.0000000\n")
   f.write("                     0.0000000 0.0000000 1.0000000\n")
f.write("   1      NUMBER OF SYMMETRY OPERATIONS\n")
f.write(" 1 0 0 0.00000000\n")
f.write(" 0 1 0 0.00000000\n")
f.write(" 0 0 1 0.00000000\n")
f.write("   1\n")   


