#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-08-05 18:13:33
# @Author  : Pan Chou (15273128925@163.com)
# @Link    : ${link}
# @Version : $Id$

import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal as sg

raw_data=pd.read_csv("F:/file/学习/专业ML/dataset/HAR/person_1/barbell bench press/01/ankle.csv",sep='\t',header=4)
data=raw_data.values
timestamp=data[:,0]
axiel=data[:,1]
t=timestamp[[i for i in range(0,100)]]
a=axiel[[i for i in range(0,100)]]
plt.plot(t,a,c='red')
plt.show()
print(timestamp)