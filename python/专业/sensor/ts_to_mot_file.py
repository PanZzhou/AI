#摄像机系统数据文件转换成opensim中的motion数据.mot文件，从而可以导入opensim中查看其运动过程
#注意：生成的.mot文件必须放入C:\Users\xinx-pc\Documents\OpenSim\4.1\Models对应的文件夹下才能加载到opensim软件中去，其他文件夹无法加载
#改进：opensim软件可以直接使用marker标记点的坐标位置信息，文件后缀为'.trc',只需讲'.ts'文件稍微做下变化即可（deal_file_cordinate函数不需使用了，作废）
import pandas as pd 
import numpy as np
import os
import re
import math

def make_dir(path):
	ex = os.path.exists(path)
	if not ex:
		os.makedirs(path)

#提取数据文件中的踝关节和膝关节的角度信息，写入opensim的motion文件
def deal_file_angle(folder,file,data):
	new_folder = folder + 'angle'
	make_dir(new_folder)
	row = data.shape[0]
	#处理数据
	time = data[:,1].reshape(row,1)
	knee_angle_r = - data[:,138].reshape(row,1)
	ankle_angle_r = (data[:,139]).reshape(row,1)-90
	knee_angle_l = - data[:,136].reshape(row,1)
	ankle_angle_l = (data[:,137]).reshape(row,1)-90
	#写数据
	match = re.search('\.ts',file)
	if match:
		index = match.span()
		out_file = new_folder+'\\'+file[0:index[0]]+'.mot'
		Columns = ['time', 'knee_angle_r','ankle_angle_r','knee_angle_l','ankle_angle_l']
		header = pd.DataFrame([['gait'],['version=1'],['nRows='+str(row)],['nColumns='+str(len(Columns))],['inDegrees=yes'],['endheader']])
		header.to_csv(out_file,index=False,header=None)
		matrix=np.hstack((time,knee_angle_r,ankle_angle_r,knee_angle_l,ankle_angle_l))
		motion = pd.DataFrame(matrix, columns=Columns)
		motion.to_csv(out_file,sep='\t',index=False,mode='a')

#提取数据文件中的p1-p12个点的坐标信息，写入opensim的motion文件
def deal_file_cordinate(folder,file,data):
	new_folder = folder + 'cordinate'
	filename = folder + file
	make_dir(new_folder)
	match = re.search('\.ts',file)
	if match:
		row = data.shape[0]
		#下面两个列表操作比较常用且高效，应熟练掌握
		raw_columns = [j+i*11 for i in range(12) for j in [2,3,4]]
		df = data[:,raw_columns]/100
		df = pd.DataFrame(df,columns=[j+str(i) for i in range(1,13) for j in ['X','Y','Z']])
		DF = pd.DataFrame()
		DF['time']=data[:,1]
		for i in range(1,13):
			#采集到的数据中，y轴和z轴和opensim的z轴和y轴分别对应
			DF['p'+str(i)] = df['X'+str(i)].apply(lambda x: '('+str(x)+' ')+df['Z'+str(i)].apply(lambda x: str(x)+' ')+df['Y'+str(i)].apply(lambda x: str(x)+')')

		index = match.span()
		out_file = new_folder+'\\'+file[0:index[0]]+'.mot'
		header = pd.DataFrame([['gait'],['version=1'],['nRows='+str(row)],['nColumns='+str(DF.shape[1])],['inDegrees=yes'],['endheader']])
		header.to_csv(out_file,index=False,header=None)
		motion = pd.DataFrame(DF)
		motion.to_csv(out_file,sep='\t',index=False,mode='a')

def deal_file_marker(folder,file,data):
	filename = folder + file
	new_folder = folder + 'marker'
	make_dir(new_folder)
	match = re.search('\.ts',file)
	if match:
		row = data.shape[0]
		raw_columns = [j+i*11 for i in range(12) for j in [2,3,4]]
		df = data[:,raw_columns]
		df = pd.DataFrame(df,columns=[j+str(i) for i in range(1,13) for j in ['X','Z','Y']])
		df[''] = data[:,1]
		df = df[['']+[j+str(i) for i in range(1,13) for j in ['X','Y','Z']]]
		#z坐标取相反数
		for z in ['Z'+str(i) for i in range(1,13)]:
			df[z]=-df[z]

		index = match.span()
		out_file = new_folder + '\\' + file[0:index[0]] + '.trc'
		p_list = ['p'+str(i) for i in range(1,13)]
		for i in range(36,0,-1):
			p_list.insert(math.ceil(i/3),'\t')
		header = pd.DataFrame([['\t'.join(['PathFileType','4','(X/Y/Z)',file[0:index[0]] + '.trc'])],
								['\t'.join(['DataRate','CameraRate','NumFrames','NumMarkers','Units','OrigDataRate','OrigDataStartFrame','OrigNumFrames'])],
								['\t'.join(['60','60',str(row),'12','mm','60','1',str(row)])],
								['Frame#\tTime\t'+''.join(p_list)]])
		header.to_csv(out_file,index=False,header=None)
		df.to_csv(out_file,sep='\t', mode='a')


def deal_folder(folder):
	path = os.listdir(folder)
	for file in path:
		if re.match('.*\.ts',file):
			raw_data = pd.read_csv(folder+file,header=5,sep='\t')
			#deal_file_angle(folder,file,raw_data.values)
			#deal_file_cordinate(folder,file,raw_data.values)
			deal_file_marker(folder,file,raw_data.values)

def deal_root_folder(root_folder):
	path = os.listdir(root_folder)
	for p in path:
		folder = root_folder+p
		if(os.path.isdir(folder)):
			deal_folder(folder+'\\')

if __name__=="__main__":
	root_folder = 'F:\\file\\学习\\专业ML\\dataset\\步态分析\\gaitAnalysis\\第2次测试\\SIAT-GAIT-8-28-2020\\'
	deal_root_folder(root_folder)
	'''
	raw_data = pd.read_csv('F:\\file\\学习\\专业ML\\dataset\\步态分析\\gaitAnalysis\\第2次测试\\SIAT-GAIT-8-28-2020\\person_4\\siat-gait-8-28-1.ts',header=5,sep='\t')
	data = raw_data.values
	df = data[:,[2,3,4]]/100
	df = pd.DataFrame(df,columns=['x1','y1','z1'])
	df['p1'] = df['x1'].apply(lambda x: '('+str(x)+' ')+df['y1'].apply(lambda x: str(x)+' ')+df['z1'].apply(lambda x: str(x)+')')
	df['time']=data[:,1]
	df[' ']=data[:,1]
	#对某一列取反
	df['x1']=-df['x1']
	print(df)
	print([j+str(i) for i in range(1,13) for j in ['x','y','z']])
	print([j+i*11 for i in range(12) for j in [2,3,4]])
	DF = pd.DataFrame()
	
	#dataframe交换两列的位置
	df[['z1','y1','x1']]
	print(['Time']+['p'+str(i) for i in range(1,13)])
	
	#在p_list列表的每个元素后面各添加三个元素'\t'
	p_list = ['p'+str(i) for i in range(1,13)]
	l=[i for i in range(1,37)]
	for i in l[::-1]:
		p_list.insert(math.ceil(i/3),'\t')
		#注意：以下是错误用法
		#p_list = p_list.insert(math.ceil(i/3),'\t')   #因为insert的返回值是None，而不是新的列表，insert直接是操作了p_list这个对象
	
	#构建逆向迭代器
	for i in range(12,0,-1):
		print(i)
	
	#把列表合为字符串，分隔符为'\t'
	p=['DataRate','CameraRate','NumFrames','NumMarkers','Units','OrigDataRate','OrigDataStartFrame','OrigNumFrames']
	print('\t'.join(p))
	'''