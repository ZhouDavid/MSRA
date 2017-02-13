# -*- coding: utf-8 -*-
import numpy as np
import os
import sys
import re
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

def write_sentences(sentences,fout):
	ss = []
	for s in sentences:
		ss.append(s+'\n')
	ls = ss[len(ss)-1]
	ls = ls.strip()
	ss[len(ss)-1] = ls
	fout.writelines(ss)
	# for s in sentences:
	# 	fout.write(s+'\n')

def split_sentence(sentence):
	sentence = sentence.strip()
	for i in ('，','！'):
		sentence = sentence.replace(i,'。')
	sentences = []
	sentences = sentence.split('。')
	return sentences

if __name__ == '__main__':
	input_path_list = ['D:\data\\raw\zizhi\origin2.txt','D:\data\\raw\zizhi\\trans2.txt']
	output_path_list=['split_origin.txt','split_trans.txt']
	# for i,path in enumerate(input_path_list):
	# 	file = open(path,'r')
	# 	fout = open(output_path_list[i],'w')
	# 	for line in file.readlines():
	# 		line = unicode(line)
	# 		sentences = split_sentence(line)
	# 		write_sentences(sentences,fout)
	# 		#write_split_line(sline,fout)
	# 	file.close()
	# 	fout.close()
	fin1 = open(input_path_list[0],'r')
	fin2 = open(input_path_list[1],'r')
	fout1 = open(output_path_list[0],'w')
	fout2 = open(output_path_list[1],'w')

	origin_sentences = fin1.readlines()
	trans_sentences = fin2.readlines()
	if len(origin_sentences)==len(trans_sentences):
		length = len(origin_sentences)
		for i in range(length):
			origin_split_sentences = split_sentence(origin_sentences[i])
			trans_split_sentences = split_sentence(trans_sentences[i])
			if len(origin_split_sentences) == len(trans_split_sentences):
				write_sentences(origin_split_sentences,fout1)
				write_sentences(trans_split_sentences,fout2)

