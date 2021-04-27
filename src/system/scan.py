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
from scipy import interpolate
import codecs
import math

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


def veto(filename,n):
    data = readData(filename, n)
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

def show(filename,n):
    I = np.array(readData(filename, n))
    t = [i*0.5 for i in range(len(I))]
    t = np.array(t)
    boolList = veto(filename,n)
    new_I = []
    new_t = []
    for i in range(len(t)):
        if boolList[i] == 0:
            new_I.append(I[i])
            new_t.append(t[i])
    z1 = np.polyfit(new_t, new_I, 1)
    p1 = np.poly1d(z1)
    yvals = p1(new_t)
    return [np.mean(new_I),np.std(new_I,ddof=1)/math.sqrt(len(new_I))]
def Qe(wave):
    wavelength=np.array(readData("../../data/pd_qe_calib.txt",0))
    Q=np.array(readData("../../data/pd_qe_calib.txt",1))
    f=interpolate.interp1d(wavelength,Q,kind="cubic")
    return (f(wave))
if __name__=='__main__':
    filepath="../../data/Ham/system/scan/"
    filepath2='../data/Ham/sipm/'
    wavelength=[]
    for i in range(9):
        wavelength.append(int(140+2*i))
    wavelength.append(int(157))
    wavelength.append(int(158))
    for j in range(4):
        wavelength.append("%.1f"%(158.2+0.2*j))
    wavelength.append(int(159))
    for k in range(9):
        wavelength.append("%.1f"%(159.1+0.1*k))
    for n in range(11):
        wavelength.append(int(160+n))
    for m in range(14):
        wavelength.append(int(172+2*m))
    #for w in wavelength:
    wavelength=np.array(wavelength)
    Qe=Qe(wavelength)
    I=[]
    x=[]
    for w in range(len(wavelength)):
        x.append(float(wavelength[w]))
        I.append(float(show(filepath+str(wavelength[w])+".TXT",2)[0]/Qe[w]))
    I=np.array(I)
    I=I/I.max()
    plt.plot(x,I,'g.')
    plt.xlabel("Wavelength [nm]")
    plt.ylabel("Relative strength")
    plt.savefig("../../resluts/ScanWavelength.png")
    print(type(x[0]))


