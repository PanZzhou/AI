import csv   #自带csv模块
import pandas as pd  #利用pandsa模块读取处理数据
import numpy as np
datas = [['name', 'age'],
         ['Bob', 14],
         ['Tom', 23],
        ['Jerry', '18']]
###csv方法
with open('example.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for row in datas:
        writer.writerow(row)
    #或者用：writer.writerows(datas)

data1=[]
with open('example.csv','r',encoding='utf-8') as f:
    reader=csv.reader(f)
    for item in reader:
        data1.append(item)
print(data1)

#pandas方法,读取csv文件
raw_data=pd.read_csv('G:/git_code/ML/LearningML/StatisticalLearningMethod/data/train_binary1.csv', header=0)
data=raw_data.values  #去除csv文件的数据部分
labels=data[:,0]     #去第一列的所有数据，类别labels存储在csv文件的第一列，":"表示所有数据，","前表示行，","后表示列
img=data[0:, 1:]   #表示从第1行第二列开始的所有数据
mn=np.array([1,1,1,1]).shape  #输出矩阵有多少行多少列
print(labels[labels==0])  #取出labels中值为0的元素
labels1=np.array(labels.flat)  #拉平矩阵
print(labels[[0,1,2,3,4,5,6,7,8]])   #根据[]内列表的元素值，把元素值当作下标重组成列表