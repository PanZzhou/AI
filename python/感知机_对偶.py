#《统计学习方法》李航著，P34例2.2
#使用感知机的对偶形式对数据进行分类
#《统计学习方法》李航著，P34例2.2
#使用感知机的对偶形式对数据进行分类
#划分整个平面的点（纵坐标不是待预测量）
import numpy as np
from numpy import *
import matplotlib.pyplot as plt 

# 数据集大小 即20个数据点
m = 30
# 横坐标坐标以及对应的向量
X1 = np.concatenate((np.random.randint(2,9,size=m//2),np.random.randint(12,18,size=m//2))).reshape(m,1) 
# 对应的纵坐标
X2 = np.concatenate((np.random.randint(5,10,size=m//2),np.random.randint(10,16,size=m//2))).reshape(m,1)

#类别
Y=ones((m,1))

#标记前一半点为正类，后一半为负类
for i in range(len(Y)):
    if i>=m//2:
        Y[i]=-Y[i]

X=hstack((X1,X2))                #坐标整合,参数为tuple
Gram=dot(X,X.transpose())        #Gram矩阵

eta=1                            #学习率

def Perceptron(Gram,Y,eta):
    alpha=ones((m,1))
    b=0
    i=0
    AlY=array([alpha[i]*Y[i] for i in range(m)])
    while i<m:  
        result=Y[i]*(dot(Gram[:,i],AlY)[0]+b)
        if result>0:
            i=i+1
        else:
            alpha[i]=alpha[i]+eta         #更新alpha
            b=b+eta*Y[i]      #更新b
            AlY=array([alpha[i]*Y[i] for i in range(m)])
            i=0             #从第一个点开始计算
    return alpha,b

def plot(X1,X2,Y,theta,b):
    ax=plt.subplot(111)
    PoX=[X1[i][0] for i in range(len(X1)) if Y[i]==1]
    ax.scatter(PoX,X2[0:len(PoX)],c='red')
    ax.scatter(X1[len(PoX):],X2[len(PoX):],c='blue')
    x=arange(0,20,0.2)
    w=-(theta[0]/theta[1])
    b=-(b/theta[1])
    y=w*x+b
    ax.plot(x,y)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

Alpha,b=Perceptron(Gram,Y,eta)
Alpha=array([Alpha[i]*Y[i] for i in range(m)])
theta=dot(Alpha.transpose(),X)[0]
print(theta,b)
plot(X1,X2,Y,theta,b)