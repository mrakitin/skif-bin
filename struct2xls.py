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

patternCUP = r"SPIN-UP CHARGE IN SPHERE (.{10,21})"
CUPnum= re.compile(patternCUP)
CUP=CUPnum.findall(data)

patternCDN = r"SPIN-DN CHARGE IN SPHERE (.{21})"
CDNnum= re.compile(patternCDN)
CDN=CDNnum.findall(data)

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

for i in range(len(X)):
   MMI1.append(float((MMI[-len(X)+i]).split(None,3)[2]))


CUP1=[]
CDN1=[]   
   
for i in range(len(X)):
   CUP1.append(float((CUP[-len(X)+i]).split()[2]))
   CDN1.append(float((CDN[-len(X)+i]).split()[2]))
 
font0 = xlwt.Font()
font0.name = 'Times New Roman'
#font0.colour_index = 2
font0.bold = True

style0 = xlwt.XFStyle()
style0.font = font0

wb = xlwt.Workbook()
ws = wb.add_sheet(name)
ws.write_merge(1, 1, 1, 7, name)
ws.write_merge(2,3,1,1,'atom number')
ws.write_merge(2,3,2,2, 'x')
ws.write_merge(2,3,3,3, 'y')
ws.write_merge(2,3,4,4, 'z')
ws.write_merge(2,3,5,5, 'magnetic moment')
ws.write_merge(2,2,6,7,'charge in sphere')
ws.write(3,6, 'up')
ws.write(3,7, 'dn')
ws.write_merge(len(X)+5,len(X)+5,1,4,'SPIN MAGNETIC MOMENT IN CELL =')
ws.write(len(X)+5,5,MMC[-1])
ws.write_merge(len(X)+6,len(X)+6,1,4,'MAGNETIC MOMENT IN INTERSTITIAL =')
ws.write(len(X)+6,5,MMII[-1])
for i in range(len(X)):
    ws.write(i+4,1,i+1)
    ws.write(i+4,2,X[i])
    ws.write(i+4,3,Y[i])
    ws.write(i+4,4,Z[i])
    ws.write(i+4,5,MMI1[i])
    ws.write(i+4,6,CUP1[i])
    ws.write(i+4,7,CDN1[i])

wb.save(path+'/%s.xls'%name)

