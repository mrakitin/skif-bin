#!/usr/bin/env python

import re
import os
import xlwt

path=os.getcwd()

name=os.path.basename(path)

data = file(path+"/%s.scf"%name).read()

patternE = r"TOTAL ENERGY IN Ry =       (.{15})"
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


data = file(path+"/%s.struct"%name).read()

file=open(path+"/%s.struct"%name,'r')
line=file.readlines()
a=float((line[3].split())[0])
b=float((line[3].split())[1])
c=float((line[3].split())[2])

name=(line[0].split())[0]

patternX = r"X=(.{10})"
Xnum= re.compile(patternX)
X=Xnum.findall(data)

patternY = r"Y=(.{10})"
Ynum= re.compile(patternY)
Y=Ynum.findall(data)

patternZ = r"Z=(.{10})"
Znum= re.compile(patternZ)
Z=Znum.findall(data)

for i in range(len(X)):
   X[i]=float(X[i])
   Y[i]=float(Y[i])
   Z[i]=float(Z[i])

for i in range(len(E)):
   E[i]=float(E[i])
   MMC[i]=float(MMC[i])
   MMII[i]=float(MMII[i])   

MMI1=[]
sum=[0.]
sum1=[0.]
sum2=[0.]
sum3=[0.]
for i in range(len(X)):
   MMI1.append(float((MMI[-len(X)+i]).split(None,3)[2]))

for i in range(len(X)):
    if abs(MMI1[i-1]) > 1:
        M=sum[-1]+abs(MMI1[i-1])
        sum.append(M)
    else : 
        L=sum1[-1]+MMI1[i-1]
        sum1.append(L)
print 'sredniy magnitnyi moment na atom Fe', M/49
print 'sredniy magnitniy moment na atom Ni', L/23
print 'magnitniy moment na superyacheiku', M+L

