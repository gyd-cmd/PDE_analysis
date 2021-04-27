# /usr/bin/env python
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


def veto(filename, n):
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


def readPD(filename, n=2):
    I = np.array(readData(filename, n))
    t = [i*0.5 for i in range(len(I))]
    t = np.array(t)
    boolList = veto(filename, n)
    new_I = []
    new_t = []
    for i in range(len(t)):
        if boolList[i] == 0:
            new_I.append(I[i])
            new_t.append(t[i])
    z1 = np.polyfit(new_t, new_I, 1)
    p1 = np.poly1d(z1)
    yvals = p1(new_t)
    return [np.mean(new_I), np.std(new_I, ddof=1)/math.sqrt(len(new_I))]


def readSipm(filename, voltage):
    I = (readData(filename, 4))
    v = (readData(filename, 2))
    new_I = []
    for i in range(len(I)):
        k = ("%.2f" % v[i])
        if k == voltage:
            new_I.append(I[i])
        else:
            pass
    new_I = np.array(new_I)
    return [np.mean(new_I), np.std(new_I, ddof=1)/math.sqrt(len(new_I))]


def cauPDE(PD_dark, SiPM_dark, PD, SiPM, Qe):
    pde = (SiPM-SiPM_dark)/(PD-PD_dark)*Qe
    return pde


if __name__ == '__main__':
    filepath = "../data/Ham/PD/"
    import matplotlib.pyplot as plt
    filepath2 = '../data/Ham/sipm/'
    wavelength = [170, 172, 174, 175, 176, 178, 180]
    Qe = [0.7979, 0.7742, 0.7525, 0.7429, 0.7334, 0.7168, 0.7012]
    Error = [0.072, 0.047, 0.0228, 0.026, 0.03, 0.019, 0.011]
    voltage = ["%.2f" % (i+1) for i in range(51)]
    for j in range(10):
        voltage.append("%.2f" % (51.1+0.1*j))
    for i in range(7):
        voltage.append("%.2f" % (53+i))
    PD_dark = readPD(filepath+"/dark/dark.txt")[0]
    # PDE results vs voltage at different wavelength.

    i = int(0)
    I_dark = []
    for var in voltage:
        SiPM_dark = (readSipm(filepath2+"/dark/dark.txt", var)[0])
        I_dark.append(SiPM_dark)
    plt.figure()
    plt.plot(voltage, I_dark, '.-')
    ax = plt.gca()
    x_major_locator = MultipleLocator(10)
    xminorLocator = MultipleLocator(1)
    ax.xaxis.set_major_locator(x_major_locator)
    ax.xaxis.set_minor_locator(xminorLocator)
    plt.xlabel("Voltage [V]")
    plt.ylabel("HPK Dark Current [A]")
    plt.yscale("log")
    plt.savefig("../resluts/Ham_dark.png")
# PDE results vs wavelength at 52V.
