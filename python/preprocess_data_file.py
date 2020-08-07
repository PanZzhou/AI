#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-08-05 15:46:34
# @Author  : Pan Chou (15273128925@163.com)
# 修改数据文件中的空格为tab
file_name='F:\\code\\sublimeCode\\python\\data\\support_vector.csv'

with open(file_name,'r+') as f:
	str=""
	for line in f.readlines():	#读取每一行
		l=line.strip().split()	#提取每一行的单词返回成列表，split()中无参数默认为所有的空字符，包括空格、换行(\n)、制表符(\t)等
		str=str+('\t'.join(l))+'\n'	#把列表中的元素连接在一起，间隔的字符为'\t'，并添加换行符
	f.truncate()	#清空文件
	f.seek(0)	#文件定位到开头
	f.write(str)	#开始写文件(覆盖原文件)
	print("操作成功")