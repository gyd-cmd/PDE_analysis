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
            if not lines:
                break
            try:
                Data.append(float(lines.split()[int(i)]))  
            except:
                pass
    return Data
def veto(filename):
    data=readData(filename)
    data=np.array(data)
    dataMean=np.mean(data)
    dataStd=np.std(data,ddof=1)
    boolList=np.zeros(len(data))
    for i in range (len(data)):
        if np.abs(data[i]-dataMean)>2*dataStd and var<=len(data)-5:
            for var in range(10):
                boolList[i-5+var]=1
        elif np.abs(data[i]-dataMean)>2*dataStd and var>len(data)-5:
            for var in range(5):
                boolList[i-5+var]=1
        else:
            pass
    print(boolList)
    newData=[]
    for i in range (len(data)):
        if boolList[i]==0:
            newData.append(data[i])
    return newData
import matplotlib.pyplot as plt
I=np.array(readData("../data/sipm/Round2/PD/Inside.TXT",2))
t=np.array(readData("../data/sipm/Round2/PD/Inside.TXT",0))
I2=np.array(readData("../data/sipm/Round2/PD/Inside2.TXT",2))
t2=[]
for i in range(len(I2)):
    t2.append(t[-1]+0.5*i)
plt.plot(t,I,label="PD")
plt.ylim(6.15e-8,6.25e-8)
plt.legend()
plt.plot(t2,I2)
plt.ylabel("$I_{PD_inside} [A]$")
plt.xlabel("time [s]")
plt.savefig("systemTest.png")

