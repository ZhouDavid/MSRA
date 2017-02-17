#-*- coding:utf-8 -*-
import chardet
def similarity(origin_sentence,trans_sentence):
	num = 0
	step = 3
	origin_sentence
	for char in origin_sentence:
		if char in trans_sentence:
			num+=1
	return (float(num)/float(len(origin_sentence)))
	
if __name__ == '__main__':
	file = open('tmp.txt')
	line = file.readlines()[0]
	file2 = open('D:\MSRA\dataset\\raw\\twenty_four_history\origin\\beiqishu2.txt')
	line2 = file2.readlines()[0]
	print len(unicode(line2))
	print similarity(line,line2)
