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
import math

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
if __name__=='__main__':
    filepath="../data/Ham/PD/round1/"
    filepath2='../data/Ham/sipm/'
    wavelength=[170,172,174,175,176,178,180]
    for w in wavelength:
        print(show(filepath+"正式测量/"+str(w)+"nm.txt",2))
