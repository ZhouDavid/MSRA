#-*- coding:utf-8 -*-
import chardet
#in_origin_path = 'E:\MSRA\dataset\\twenty_four_history\\total_origin\shiji.txt'
in_origin_path = 'E:\MSRA\dataset\\twenty_four_history-v2\origin\shiji.txt'
in_trans_path = 'E:\MSRA\dataset\\twenty_four_history\\total_trans\shiji.txt'
out_origin_path = 'E:\MSRA\dataset\\twenty_four_history\shiji\shiji_origin.txt'
out_trans_path = 'E:\MSRA\dataset\\twenty_four_history\shiji\shiji_trans.txt'


def find_title(line,titles):
	for i,title in enumerate(titles):
		if not line.find(title)==-1:
			return i
	return -1

def deal_with_shiji_origin(in_origin_path,out_origin_path,in_trans_path,out_trans_path):
	'''
	处理原文
	'''
	file = open(in_origin_path,'r')
	lines = file.readlines()
	file.close()
	titles = []
	context = lines[0:len(lines)]  #正文
	paras = []
	para = ''
	for line in context:
		#title_index = find_title(line,origin_category)
		index = line.find('●')
		if not index ==-1:
			if len(para)>0:
				paras.append(para+'</p>\n')
				para = ''
			#cur_title = origin_category[title_index]
			cur_title = line[index+3:len(line)]
			titles.append(cur_title)
			line = '<p>'+'<title>'+cur_title.strip()+'</title>'
			para+=line.strip()
		else:
			para+=line.strip()
	paras.append(para)
	file = open(out_origin_path,'w')
	file.writelines(paras)
	file.close()

	'''
	处理译文
	'''
	def is_title(line):
		for title in titles:
			start = title.find('·')+2
			end = title.find('第')
			title= title[start:end]
			if line.startswith(title):
				return end-start
		return -1

	file=open(in_trans_path,'r')
	lines = file.readlines()
	file.close()
	para =''
	paras=[]

	for line in lines:
		name_length = is_title(line)
		if name_length>0:
			if len(para)>0:
				paras.append(para+'</p>\n')

			para ='<p>'+'<title>'+line[0:name_length]+'</title>'+line[name_length:len(line)].strip()
		else:
			para+=line.strip() 
	paras.append(para)
	file=open(out_trans_path,'w')
	file.writelines(paras)
	file.close()


if __name__ == '__main__':
	deal_with_shiji_origin(in_origin_path,out_origin_path,in_trans_path,out_trans_path)
	# s = '卷一·五帝本纪第一'
	# start = s.find('·')
	# end = s.find('第')
	# print(start,end)
	# f=open('tmp.txt','w')
	# f.write(s[start+2:end])