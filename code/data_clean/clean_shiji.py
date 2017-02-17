#-*- coding:utf-8 -*-
import chardet
import pdb
#in_origin_path = 'E:\MSRA\dataset\\twenty_four_history\\total_origin\shiji.txt'
in_origin_path = 'D:\MSRA\dataset\\raw\\twenty_four_history-v2\origin\shiji.txt'
in_trans_path = 'D:\MSRA\dataset\\raw\\twenty_four_history-v2\\trans\shiji.txt'
out_origin_path = 'D:\MSRA\dataset\\raw\\twenty_four_history\shiji\shiji_origin.txt'
out_trans_path = 'D:\MSRA\dataset\\raw\\twenty_four_history\shiji\shiji_trans.txt'


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
		index = line.find('●')
		if not index ==-1:
			if len(para)>0:
				paras.append(para+'</p>\n')
				para = ''
			#cur_title = origin_category[title_index]
		
			cur_title = line[index+3:len(line)]
			titles.append(cur_title)
			start = cur_title.find('·')+2
			end = cur_title.find('第')
			cur_title= cur_title[start:end]

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
	got_titles=[]
	def is_title(line):
		for title in titles:
			start = title.find('·')+2
			end = title.find('第')
			title= title[start:end]
			if line.startswith(title):
				got_titles.append(title+'\n')
				return end-start
		return -1

	file=open(in_trans_path,'r')
	lines = file.readlines()
	file.close()
	para =''
	paras=[]
	title_num = 0
	for line in lines:
		name_length = is_title(line)
		if name_length>0:
			title_num+=1
			if len(para)>0:
				paras.append(para+'</p>\n')

			para ='<p>'+'<title>'+line[0:name_length]+'</title>'+line[name_length:len(line)].strip()
		else:
			para+=line.strip()
	print title_num
	paras.append(para)
	file=open(out_trans_path,'w')
	file.writelines(paras)
	file.close()

	leak = []
	clean_titles=[]
	for title in titles:
		start = title.find('·')+2
		end = title.find('第')
		title= title[start:end]
		clean_titles.append(title+'\n')

	'''
	筛选出在译文中的篇目
	'''
	# for i in clean_titles:
	# 	if not i in got_titles:
	# 		leak.append(i)
	# file = open('tmp.txt','w')
	# file.writelines(leak)
	# file.close()
def abstract_title(line):
	start = line.find('<title>')
	end = line.find('</title>')
	start += 7
	title = line[start:end]
	return title

def abstract_content(line):
	start = line.find('</title>')+8
	end = line.find('</p>')
	return line[start:end]

def generate_trans_pair(in_origin_path,in_trans_path,out_origin_path,out_trans_path):
	fin1 = open(in_origin_path,'r')
	fin2 = open(in_trans_path,'r')
	origin_lines = fin1.readlines()
	trans_lines = fin2.readlines()
	fin1.close()
	fin2.close()
	i = 0

	fout1 = open(out_origin_path,'w')
	fout2 = open(out_trans_path,'w')

	for j,trans_line in enumerate(trans_lines):
		trans_title = abstract_title(trans_line)
		cur_origin_title = abstract_title(origin_lines[i])

		while not trans_title == cur_origin_title:
			i+=1
			try:
				cur_origin_title = abstract_title(origin_lines[i])
			except:
				print i,j
				input()

		trans_content = abstract_content(trans_line)
		origin_content = abstract_content(origin_lines[i])
		trans_sentences = trans_content.split('。')
		origin_sentences = origin_content.split('。')
		origin_sentences = map(lambda s:s+'。\n',origin_sentences)
		trans_sentences=map(lambda s:s+'。\n',trans_sentences)
		fout1.writelines(origin_sentences)
		fout2.writelines(trans_sentences)
		i+=1

	fout1.close()
	fout2.close()




	

if __name__ == '__main__':
	#deal_with_shiji_origin(in_origin_path,out_origin_path,in_trans_path,out_trans_path)
	generate_trans_pair('D:\MSRA\dataset\\raw\\twenty_four_history\shiji\shiji_origin.txt',\
		'D:\MSRA\dataset\\raw\\twenty_four_history\shiji\shiji_trans.txt',\
		'D:\MSRA\dataset\\raw\\twenty_four_history\shiji\shiji_origin_split.txt',\
		'D:\MSRA\dataset\\raw\\twenty_four_history\shiji\shiji_trans_split.txt')
	# # s = '卷一·五帝本纪第一'
	# start = s.find('·')
	# end = s.find('第')
	# print(start,end)
	# f=open('tmp.txt','w')
	# f.write(s[start+2:end])