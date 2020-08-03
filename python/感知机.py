#划分整个平面的点（纵坐标不是待预测量）
from numpy import *

# 数据集大小 即20个数据点
m = 20
k=2
n = random.randint(1,m-k-1)
# 横坐标坐标以及对应的矩阵
X1 = arange(1, m+1).reshape(m, 1)  # 生成一个m行1列的向量，也就是x1，从1到m
# 对应的纵坐标
X2 = array([
    3, 4, 5, 5, 2, 4, 7, 8, 11, 8, 12,
    11, 13, 13, 16, 17, 18, 17, 19, 21
]).reshape(m, 1)

#类别
Y=ones((m,1))

Filter=[True]*m
k1=k
while k1>0:
    Filter[n]=False
    n=n+1
    k1=k1-1
#处理掉多余数据，让其看上去出现两类
X1=X1[Filter]
X2=X2[Filter]
Y=Y[Filter]
X=hstack((X2,X1,Y))

Y[n:-1]=-1
Y[len(Y)-1]=-1
# 学习率
eta = 1

#挨个挨个数据试
def Perceptron(X,Y,eta):
    i=0
    theta=array([1,-1,0]).reshape(3,1)
    while (i<m-k):
        result=Y[i]*dot(X[i],theta)
        if result<=0:
            theta=theta+eta*Y[i]*X[i].reshape(3,1)
            i=0
        else:
            i=i+1
    return theta


def plot(X,Y,theta):
    import matplotlib.pyplot as plt
    ax = plt.subplot(111)
    ax.scatter(X,Y,c='red')
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
print(n)
plot(X1,X2,optimal)