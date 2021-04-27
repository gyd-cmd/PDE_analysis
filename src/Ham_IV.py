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
    import matplotlib.pyplot as plt
    plt.style.use("my")
    SiPM = np.array(
        readData("../data/Ham/HPK_decline/175NM-2-HPK.TXT", 4))
    SiPM2 = np.array(
        readData("../data/Ham/HPK_decline/175NM-3-HPK.TXT", 4))
    SiPM3 = np.array(
        readData("../data/Ham/HPK_decline/400NM-7-HPK.TXT", 4))
    SiPM4 = np.array(
        readData("../data/Ham/HPK_decline/400NM-9-HPK.TXT", 4))
    t = [i*0.5 for i in range(len(SiPM))]
    plt.figure()

    ax = plt.gca()
    x_major_locator = MultipleLocator(100)
    xminorLocator = MultipleLocator(20)
    # yminorLocator = MultipleLocator(0.2)
    # ax.xaxis.set_major_locator(x_major_locator)
    # ax.yaxis.set_major_locator(yminorLocator)
    # ax.xaxis.set_minor_locator(xminorLocator)
    y = []
    x = []
    y2 = []
    y3 = []
    y4 = []
    for i in range(int(len(SiPM)/60)):
        y.append(np.mean(SiPM[i*60:i*60+60]))
        x.append(0.5*i)
        y2.append(np.mean(SiPM2[i*60:i*60+60]))
        y3.append(np.mean(SiPM3[i*60:i*60+60]))
        y4.append(np.mean(SiPM4[i*60:i*60+60]))
    plt.plot(x, y/y[0], '.-', markersize=5, label="175nm Low intensity")
    plt.plot(x, y4/y4[0], '.-', markersize=5, label="400nm Low intensity")
    plt.plot(x, y2/y2[0], '.-', markersize=5, label="175nm High intensity")
    plt.plot(x, y3/y3[0], '.-', markersize=5, label="400nm High intensity")

    plt.xlabel("t [min]")
    plt.ylabel("Normalized $I_{HPK}$")
    plt.legend(loc='center')
    plt.show()
