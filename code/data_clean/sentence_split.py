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
	sentences = map(lambda x:x.encode('utf-8')+u'。\n',sentences)
	for s in sentences:
		if len(s)>2:
			ss.append(s)
	fout.writelines(ss)


def split_sentence(sentence):
	sentence = unicode(sentence).strip()
	sentences = []
	sentences = sentence.split(u'。')
	return sentences

if __name__ == '__main__':
	input_path_list = ['D:\MSRA\dataset\\raw\zizhitongjian\origin8.txt','D:\MSRA\dataset\\raw\zizhitongjian\\trans8.txt']
	output_path_list=['D:\MSRA\dataset\\raw\zizhitongjian\\split_origin8.txt','D:\MSRA\dataset\\raw\zizhitongjian\\split_trans8.txt']
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

	origin_sentences = map(lambda x:x.decode('utf-8').strip(),origin_sentences)
	trans_sentences = map(lambda x:x.decode('utf-8').strip(),trans_sentences)

	if len(origin_sentences)==len(trans_sentences): #理论上应该是相等的，因为句子数量是一样的
		length = len(origin_sentences)   
		for i in range(length):
			origin_split_sentences = split_sentence(origin_sentences[i])
			trans_split_sentences = split_sentence(trans_sentences[i])
			if len(origin_split_sentences) == len(trans_split_sentences):#split出来的数量相等才保留
				write_sentences(origin_split_sentences,fout1)
				write_sentences(trans_split_sentences,fout2)
			else:
				fout1.write(origin_sentences[i].encode('utf-8')+'\n')
				fout2.write(trans_sentences[i].encode('utf-8')+'\n')


