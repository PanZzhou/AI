#《统计学习方法》李航著，P34例2.2
#使用感知机的对偶形式对数据进行分类
from numpy import *
import matplotlib.pyplot as plt 

X1=array([3,4,1]).reshape(3,1)   #横坐标
X2=array([3,3,1]).reshape(3,1)   #纵坐标
Y=array([1,-1,1]).reshape(3,1)   #分类

X=hstack((X1,X2))                #坐标整合,参数为tuple
Gram=dot(X,X.transpose())        #Gram矩阵

eta=1                            #学习率

def Perceptron(Gram,Y,eta):
    alpha=zeros((3,1))
    b=0
    i=0
    AlY=array([alpha[i]*Y[i] for i in range(3)])
    while i<3:
        result=Y[i]*(dot(Gram[:,i],AlY)[0]+b)
        if result>0:
            i=i+1
        else:
            alpha[i]=alpha[i]+eta         #更新alpha
            b=b+eta*Y[i]      #更新b
            AlY=array([alpha[i]*Y[i] for i in range(3)])
            i=0             #从第一个点开始计算
    return alpha,b

def plot(X1,X2,theta,b):
    ax=plt.subplot(111)
    ax.scatter(X1,X2,c='red')
    x=arange(0,7,0.2)
    w=-(theta[0]/theta[1])
    b=-(b/theta[1])
    y=w*x+b
    ax.plot(x,y)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

Alpha,b=Perceptron(Gram,Y,eta)
Alpha=array([Alpha[i]*Y[i] for i in range(3)])
theta=dot(Alpha.transpose(),X)[0]
print(theta)
plot(X1,X2,theta,b)