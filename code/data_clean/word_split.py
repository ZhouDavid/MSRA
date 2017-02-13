# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def naive_split(line):
	'''无脑按照空格分所有词'''
	line = unicode(line)
	ans=[]
	for i in range(len(line)):
		ans.append(line[i])
	return ans

def write_split_line(sline,fout):
	line=''
	for ch in sline:
		line = line+ch+' '
	line = line.strip()
	fout.write(line+'\n')

input_path = ['split_origin.txt','split_trans.txt']
output_path = ['word_split_origin.txt','word_split_trans.txt']


for i,path in enumerate(input_path):
	fin = open(path,'r')
	fout = open(output_path[i],'w')
	for line in fin.readlines():
		sline = naive_split(line)
		write_split_line(sline,fout)






