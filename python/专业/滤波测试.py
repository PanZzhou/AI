#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-08-05 18:13:33
# @Author  : Pan Chou (15273128925@163.com)
# @Link    : ${link}
# @Version : $Id$

import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal as sg
import dtcwt
import numpy as np
#import pywt
from matplotlib.pylab import *
import scipy.signal as signal


#raw_data=pd.read_csv("F:/file/学习/专业ML/dataset/HAR/person_1/barbell bench press/01/ankle.csv",sep='\t',header=4)
raw_data=pd.read_csv("F:\\file\\学习\\专业ML\\dataset\\步态分析\\gaitAnalysis\\2020-08-25_14.30.39_gaitAnalysis_MultiSession\\gaitAnalysis_Session1_ankle_Calibrated_PC.csv",sep='\t',header=3)
data=raw_data.values
timestamp=data[:,0]
axiel=data[:,1]#加速度x轴数据
gyro_data=data[:,9]#陀螺仪z轴数据

t=timestamp
#中值滤波
#a=signal.medfilt(axiel,5)
#g=signal.medfilt(gyro_data,5)
a=axiel
g=gyro_data

#切比雪夫二型滤波
sos = signal.cheby2(4, 20, 0.3, 'lowpass', output='sos')
a_filtered = signal.sosfilt(sos, a)
plt.figure(figsize=(12, 12))
subplot(211)
plot(t,a_filtered)
subplot(212)
plot(t,a)
# subplot(212)
#plot(t,g)
show()
print(len(a))
print(len(a_filtered))

#小波变换
'''
coeffs = pywt.wavedec(a, 'db4', level=4) # 4阶小波分解
ya4 = pywt.waverec(np.multiply(coeffs, [1, 0, 0, 0, 0]).tolist(), 'db4')
yd4 = pywt.waverec(np.multiply(coeffs, [0, 1, 0, 0, 0]).tolist(), 'db4')
yd3 = pywt.waverec(np.multiply(coeffs, [0, 0, 1, 0, 0]).tolist(), 'db4')
yd2 = pywt.waverec(np.multiply(coeffs, [0, 0, 0, 1, 0]).tolist(), 'db4')
yd1 = pywt.waverec(np.multiply(coeffs, [0, 0, 0, 0, 1]).tolist(), 'db4')
plt.figure(figsize=(12, 12))
plt.subplot(611)
plt.plot(t, a)
plt.title('original signal')
plt.subplot(612)
plt.plot(t, ya4)
plt.title('approximated component in level 4')
plt.subplot(613)
plt.plot(t, yd4)
plt.title('detailed component in level 4')
plt.subplot(614)
plt.plot(t, yd3)
plt.title('detailed component in level 3')
plt.subplot(615)
plt.plot(t, yd2)
plt.title('detailed component in level 2')
plt.subplot(616)
plt.plot(t, yd1)
plt.title('detailed component in level 1')
plt.tight_layout()
plt.show()
'''
#双树复小波变换
'''
#vecs = np.cumsum(np.random.rand(300,2) - 0.5, 0)
vecs = mat(a).T
plt.figure(figsize=(12, 12))
# Show input
subplot(611)
plot(vecs)
title('Input')
# 1D transform, 5 levels
transform = dtcwt.Transform1d(biort='legall',qshift='qshift_a')
vecs_t = transform.forward(vecs, nlevels=4)
# Show level 2 highpass coefficient magnitudes
subplot(612)
plot(np.abs(vecs_t.highpasses[1]))
title('Level 2 wavelet coefficient magnitudes')

# Show last level lowpass image
subplot(613)
plot(vecs_t.lowpass)
title('Lowpass signals')

# Inverse
vecs_recon = transform.inverse(vecs_t)

# Show output
subplot(614)
plot(vecs_recon)
title('Output')

# Show error
subplot(615)
plot(vecs_recon - vecs)
title('Reconstruction error')
show()

#print('Maximum reconstruction error: {0}'.format(np.max(np.abs(vecs - vecs_recon))))
'''