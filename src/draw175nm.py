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
# *************************************************************************

import matplotlib.pyplot as plt
import os
import sys
import numpy as np
import scipy
import codecs


def readData(filename, i):
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
    data = readData(filename, 2)
    data = np.array(data)
    dataMean = np.mean(data)
    dataStd = np.std(data, ddof=1)
    boolList = np.zeros(len(data))
    for i in range(len(data)):
        if np.abs(data[i]-dataMean) > 2*dataStd and i <= len(data)-5:
            for var in range(10):
                boolList[i-5+var] = 1
        elif np.abs(data[i]-dataMean) > 2*dataStd and i > len(data)-5:
            for var in range(5):
                boolList[i-5+var] = 1
        else:
            pass
    return boolList


I = np.array(readData("/Users/kanu/IHEPBox/sipmPDE/data/pd/170-180Monit/180(1).txt", 2))
t = [i*0.5 for i in range(len(I))]
t = np.array(t)
boolList = veto("/Users/kanu/IHEPBox/sipmPDE/data/pd/170-180Monit/180(1).txt")
print(I)
print(t)
new_I = []
new_t = []
for i in range(len(t)):
    if boolList[i] == 0:
        new_I.append(I[i])
        new_t.append(t[i])
z1 = np.polyfit(new_t, new_I, 1)
p1 = np.poly1d(z1)
yvals = p1(new_t)
plt.plot(new_t, yvals, "r-")
plt.plot(new_t, new_I, label="PD")
plt.text(1500, 0.15e-11, "Fit function : "+"%.2f" %
         (p1[0]*1e12)+"e-12+"+"%.2f" % (p1[1]*1e19)+"e-19*t")
print(p1[1])
plt.legend()
plt.plot(new_t, yvals, "r-")
plt.ylabel("$I_{PD} [A]$")
plt.xlabel("time [s]")
plt.show()
# plt.savefig("../resluts/stable/systemTest.png")
