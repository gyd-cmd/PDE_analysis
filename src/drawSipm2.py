#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ************************************************************************ 
# * 
# * @file:produceDate.py 
# * @author:guanyuduo@ihep.ac.cn 
# * @date:2021-03-18 15:53 
# * @version 3.6  
# * @description: Python Script 
# * @Copyright (c)  all right reserved 
# * 
#************************************************************************* 

import os,sys
import numpy as np
import scipy
import codecs
def readData(filename,i):
    Data = []
    with codecs.open(filename, 'r', encoding='gbk') as file_to_read:
        while True:
            lines = file_to_read.readline()
            print(lines.split())
            if not lines:
                break
            try:
                Data.append(float(lines.split()[int(i)]))  
            except:
                pass
    return Data
def veto(filename):
    data=readData(filename,2)
    data=np.array(data)
    dataMean=np.mean(data)
    dataStd=np.std(data,ddof=1)
    boolList=np.zeros(len(data))
    for i in range (len(data)):
        if np.abs(data[i]-dataMean)>2*dataStd and i<=len(data)-5:
            for var in range(10):
                boolList[i-5+var]=1
        elif np.abs(data[i]-dataMean)>2*dataStd and i>len(data)-5:
            for var in range(5):
                boolList[i-5+var]=1
        else:
            pass
    return boolList
import matplotlib.pyplot as plt
I=(readData("../data/Ham/sipm/正式测量/170nm.txt",4))
v=(readData("../data/Ham/sipm/正式测量/170nm.txt",2))
t=[i*0.5 for i in range(len(I))]
new_I=[]
for i in range(len(I)):
    if float(v[i]) == 52:
        new_I.append(I[i])
    else:
        pass
new_I=np.array(new_I)
plt.ylabel("I_Ham withlight[mA]")
plt.xlabel("t")

plt.plot([i for i in range(len(new_I))],new_I*1000)
#plt.show()
plt.savefig("../resluts/Ham/170nm_52V.png")
