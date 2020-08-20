#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-08-05 15:27:14
# @Author  : Pan Chou (15273128925@163.com)
# @Link    : ${link}
# @Version : $Id$

import pandas as pd
import numpy as np
from numpy import *

filename_traindata='F:\\code\\sublimeCode\\python\\data\\support_vector.csv'
raw_data=pd.read_csv(filename_traindata,header=0,sep="\t")
data=raw_data.values
#获取特征数据
features=data[:,0:2] #':'表示全部行（','前表示行，','后表示列）,取0和1列的全部数据
#获取标签数据
labels=data[:,2] #取第二列的全部数据

#取出类型为1的特征数据
fit_l=labels>0	#返回true和false组成的数组，此返回数组的元素为对labels中每个元素执行>0操作，符合返回true，反之返回false
positive_labels=labels[labels==1]
positive_features=features[labels==1]

#获取某个特征的取值范围（特征i能取几种取值）
kind_labels=set(labels)  #得出一共有两种类型
kind_feature_0=set(features[:,0])

#获取矩阵维数
n=features.shape

#生成等差数列
cha1=np.linspace(1,10,10)	#生成1-10的个数为10的等差数列
cha2=np.linspace(1,10)	#生成1-10的个数为50的等差数列

nozero=np.nonzero(labels)	#返回元素值不为零的元素下标

#####################################
a=array([1,2,3,4]).reshape(2,2)	#array是数组类型，可以为一维，二维...n维
b=array([0,1,2,3]).reshape(2,2)
c=mat(a)	#把array转换成矩阵matrix,其必须是二维及以上，array包含了matrix，array的运算matrix都有
d=mat(b)
multiply(a,b)	#数组的对应位置相乘
multiply(c,d)	#举证的对应位置相乘

dot(a[0],b[0])	#对一维数组乘完了相加
dot(a,b)	#对多维数组实行矩阵运算
dot(c,d)	#矩阵的乘法

a*b	#数组的对应位置相乘
c*d	#矩阵的乘法

#注意下面这两个的结果不一样
print(np.array([[1,2,3]]).T)
print(np.array([1,2,3]).T)