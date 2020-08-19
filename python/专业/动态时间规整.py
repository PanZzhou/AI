#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-08-14 15:21:48
# @Author  : Pan Chou (15273128925@163.com)
# @Link    : ${link}
# @Version : $Id$

from dtw import dtw
from numpy.linalg import norm
from numpy import *
from matplotlib.pyplot import *
a=array([2,3,2,3,5,1])
b=array([4,6,7,8,5,3])

dist, cost, acc_cost, path = dtw(a, b, dist=lambda x, y: abs(x - y))
print(dist)
#imshow(cost.T, origin='lower', cmap=cm.gray, interpolation='nearest')
plot(path[0], path[1])
xlim((-0.5, cost.shape[0]-0.5))
ylim((-0.5, cost.shape[1]-0.5))
show()
print(cost.shape)