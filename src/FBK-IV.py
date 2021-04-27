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
from matplotlib.pyplot import MultipleLocator


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
            print("name")
    return boolList


plt.style.use("my")
I = np.array(readData("../data/FBK_3/I-V_P20.txt", 2))
V = np.array(readData("../data/FBK_3/I-V_P20.txt", 3))
x = []
y = []
for i in range(len(V)-1):
    if V[i] != V[i+1]:
        x.append(V[i])
        y.append(I[i])
plt.plot(x, y, 'r.', label="FBK No.3 $20^{o}C$")

I = np.array(readData("../data/FBK_3/I-V_N50.txt", 2))
V = np.array(readData("../data//FBK_3/I-V_N50.txt", 3))
x = []
y = []
for i in range(len(V)-1):
    if V[i] != V[i+1]:
        x.append(V[i])
        y.append(I[i])
plt.plot(x, y, 'b.', label="FBK No.3 $-50^{o}C$")

I = np.array(readData("../data/FBK_3/I-V_N60.txt", 2))
V = np.array(readData("../data/FBK_3/I-V_N60.txt", 3))
x = []
y = []
for i in range(len(V)-1):
    if V[i] != V[i+1]:
        x.append(V[i])
        y.append(I[i])
plt.xlabel("Voltage [V]")
plt.ylabel("Dark Current of FBK [A]")
plt.legend(loc="upper left")
xminorLocator = MultipleLocator(1)  # 将x轴次刻度标签设置为5的倍数
ax = plt.gca()
ax.xaxis.set_minor_locator(xminorLocator)
plt.yscale("log")
plt.show()
