#usr/bin/env python
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
if __name__=='__main__':
    filepath="../../data/Ham/system/ratio/pd/"
    filepath2="../../data/Ham/system/ratio/sipm/"
    filenamelist=['0.41','0.87','1.1','1.5','2.1']
    I_pd=[]
    I_sipm=[]
    for var in filenamelist:
        I_pd.append((show(filepath+var+".TXT",2)[0]-show("../../data/Ham/pd/dark/dark.txt",2)[0]))
        I_sipm.append(readSipm(filepath2+var+".TXT",("%.2f"%54))[0])
        print(I_sipm[-1]/I_pd[-1])
    print(show("../../data/Ham/pd/dark/dark.txt",2)[0])
    plt.plot(I_pd,I_sipm,'b.-')
    filepath="../../data/Ham/PD/round1/正式测量/"
    filepath2="../../data/Ham/sipm/正式测量/"
    I_pd.append((show(filepath+str(175)+"nm.TXT",2)[0]-show("../../data/Ham/pd/dark/dark.txt",2)[0]))
    I_sipm.append(readSipm(filepath2+str(175)+"nm.TXT",("%.2f"%54))[0])
    plt.plot(I_pd[-1],I_sipm[-1],'r.')
    plt.xlabel("$I_{PD}$")
    plt.ylabel("$I_{SiPM}$")
    plt.savefig("../../resluts/ratio.png")

