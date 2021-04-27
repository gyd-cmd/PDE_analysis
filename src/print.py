#/usr/bin/env python
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

def show(filename):
    I = np.array(readData("/Users/kanu/IHEPBox/sipmPDE/data/Ham/PD/"+filename+".txt", 2))
    t = [i*0.5 for i in range(len(I))]
    t = np.array(t)
    boolList = veto("/Users/kanu/IHEPBox/sipmPDE/data/Ham/PD/"+filename+".txt")
    new_I = []
    new_t = []
    for i in range(len(t)):
        if boolList[i] == 0:
            new_I.append(I[i])
            new_t.append(t[i])
    z1 = np.polyfit(new_t, new_I, 1)
    p1 = np.poly1d(z1)
    yvals = p1(new_t)
    print("I_PD = "+" "+str(np.mean(new_I)))
    return np.mean(new_I)
print("Wavelength")
print("Befor sipm mesuerment PD current")
print("After sipm mesuerment PD current")
print("Eorr ")
print("180nm")
a=show("round1/正式测量/180nm")
b=show("round2/180nm")
print("Eorr = "+str((a-b)/a))
print("178nm")
a=show("round1/正式测量/178nm")
b=show("round2/178nm")
print("Eorr = "+str((a-b)/a))
print("176m")
a=show("round1/正式测量/176nm")
b=show("round2/176nm")
print("Eorr = "+str((a-b)/a))
print("175nm")
a=show("round1/正式测量/175nm")
b=show("round2/175nm")
print("174nm")
print("Eorr = "+str((a-b)/a))
a=show("round1/正式测量/174nm")
b=show("round2/174nm")
print("Eorr = "+str((a-b)/a))
print("172nm")
a=show("round1/正式测量/172nm")
b=show("round2/172nm")
print("Eorr = "+str((a-b)/a))
print("170nm")
a=show("round1/正式测量/170nm")
b=show("round2/170nm")
print("Eorr = "+str((a-b)/a))
