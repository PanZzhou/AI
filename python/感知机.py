#划分整个平面的点（纵坐标不是待预测量）
import numpy as np
from numpy import *

# 数据集大小 即20个数据点
m = 30
# 横坐标坐标以及对应的向量
X1 = np.concatenate((np.random.randint(2,9,size=m//2),np.random.randint(12,18,size=m//2))).reshape(m,1) 
# 对应的纵坐标
X2 = np.concatenate((np.random.randint(5,10,size=m//2),np.random.randint(10,16,size=m//2))).reshape(m,1)

#类别
Y=ones((m,1))

X=hstack((X2,X1,Y))

#标记前一半点为正类，后一半为负类
for i in range(len(Y)):
    if i>=m//2:
        Y[i]=-Y[i]

# 学习率
eta = 1

#挨个挨个数据试
def Perceptron(X,Y,eta):
    i=0
    theta=array([1,-1,0]).reshape(3,1)
    while (i<m):
        result=Y[i]*dot(X[i],theta)
        if result<=0:
            theta=theta+eta*Y[i]*X[i].reshape(3,1)
            i=0
        else:
            i=i+1
    return theta


def plot(X,Y,Y1,theta):
    import matplotlib.pyplot as plt
    ax = plt.subplot(111)
    PoX=[X[i][0] for i in range(len(X)) if Y1[i]==1]
    ax.scatter(PoX,Y[0:len(PoX)],c='red')
    ax.scatter(X[len(PoX):],Y[len(PoX):],c='blue')
    if theta[0]!=0:
        x=arange(1,21,0.2)
        w=-(theta[1]/theta[0])
        b=-(theta[2]/theta[0])
        y=b+w*x
        ax.plot(x,y)
    else:
        x=-(theta[2]/theta[1])
        ax.vlines(x, 0, m)  #画垂直于x轴的线
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

optimal=Perceptron(X,Y,eta)
plot(X1,X2,Y,optimal)