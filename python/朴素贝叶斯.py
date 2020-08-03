#贝叶斯是不需要学习的一种方法
from numpy import *
import random
X1=array([1]*5+[2]*5+[3]*5).reshape(15,1)
X2=array(['s','m','m','s','s',
    's','m','m','l','l',
    'l','m','m','l','l']).reshape(15,1)
Y=array([0,0,1,1,0,
         0,0,1,1,1,
         1,1,1,1,0])
X=hstack((X1,X2))
y={}
for e in Y:
    y[e]=y.get(e,0)+1

#拉普拉斯平滑
lamda=1

def needed_cnt(t,X,Y,kind):
    XY_cnt1=0
    XY_cnt2=0
    n=0
    while n<15:
        if Y[n]==kind:
            if X[n][0]==t[0]:
                XY_cnt1+=1
            if X[n][1]==t[1]:
                XY_cnt2+=1
        n=n+1
    return XY_cnt1,XY_cnt2

#极大似然估计
def naivebayes_1(t,X,Y,y):
    max=0
    flag=-1
    i=0    #既是迭代计数器，也是类别标识
    while i<2:
        cnt_1,cnt_2=needed_cnt(t,X,Y,i)
        pr_Y=y[i]/len(Y)
        pr_XY1=cnt_1/y[i]
        pr_XY2=cnt_2/y[i]
        pr_res=pr_Y*pr_XY1*pr_XY2
        if pr_res>max:
            max=pr_res
            flag=i
        i=i+1
    return max,flag

#贝叶斯估计(极大似然估计可能会出现所估计的概率值为0的情况，这会影响到后验概率的计算结果)
def naivebayes_2(t,X,Y,y,kind_x1,kind_x2):
    max=0
    flag=-1
    i=0    #既是迭代计数器，也是类别标识
    while i<2:
        cnt_1,cnt_2=needed_cnt(t,X,Y,i)
        #下三行和极大似然估计的代码不同
        pr_Y=(y[i]+lamda)/(len(Y)+len(y)*lamda)
        pr_XY1=(cnt_1+lamda)/(y[i]+len(kind_x1)*lamda)
        pr_XY2=(cnt_2+lamda)/(y[i]+len(kind_x2)*lamda)
        pr_res=pr_Y*pr_XY1*pr_XY2
        if pr_res>max:
            max=pr_res
            flag=i
        i=i+1
    return max,flag

if __name__=='__main__':
    for i in range(10):
        K1=[1,2,3]     #X1的取值种类
        K2=['s','m','l']   #X2的取值种类
        t=array([random.choice(K1),random.choice(K2)])  #随机出一个测试示例:如[2 's']
        print("随机实例：{0}".format(t))
        pr,kind=naivebayes_1(t,X,Y,y)    #极大似然估计
        print("    极大似然：以{0:.4f}的概率被预测为{1}类".format(pr,kind))
        pr,kind=naivebayes_2(t,X,Y,y,K1,K2)   #贝叶斯估计
        print("    贝叶斯：以{0:.4f}的概率被预测为{1}类".format(pr,kind))