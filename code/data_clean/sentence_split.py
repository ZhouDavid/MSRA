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


	# ls = ss[len(ss)-1]
	# ls = ls.strip()
	# ss[len(ss)-1] = ls
	fout.writelines(ss)
	# for s in sentences:
	# 	fout.write(s+'\n')

def split_sentence(sentence):
	sentence = unicode(sentence).strip()
	#sentence = sentence.strip()
	for i in ('，','。'):
		sentence = sentence.replace(i,i+' ')
	sentences = []
	sentences = sentence.split()
	return sentences

if __name__ == '__main__':
	input_path_list = ['D:\data\\raw\zizhi\origin2.txt','D:\data\\raw\zizhi\\trans2.txt']
	output_path_list=['D:\data\clean\zizhitongjian\\split_origin2.txt','D:\data\clean\zizhitongjian\\split_trans2.txt']
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
	if len(origin_sentences)==len(trans_sentences):  #理论上应该是相等的，因为句子数量是一样的
		length = len(origin_sentences)   
		for i in range(length):
			origin_sentence = unicode(origin_sentences[i])
			trans_sentence = unicode(trans_sentences[i])
			# if len(origin_sentence)>=10 and len(origin_sentence)<=50:#如果句子长度不是很长就不split了
			# 	write_sentences([origin_sentence],fout1)
			# 	write_sentences([trans_sentence],fout2)
	
			origin_split_sentences = split_sentence(origin_sentence)
			trans_split_sentences = split_sentence(trans_sentences[i])
			if len(origin_split_sentences) == len(trans_split_sentences):#split出来的数量相等才保留
				write_sentences(origin_split_sentences,fout1)
				write_sentences(trans_split_sentences,fout2)

