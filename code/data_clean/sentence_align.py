#-*-coding:utf-8 -*-

charset = u'，。,：?、”“—.！!》《\n'
import sentence_sim
import pdb

#origin_sentence
def find_match_index(origin_sentence,origin_id,trans_set):
	start = -1
	end = -1
	origin_sentence = sentence_sim.multiple_replace(origin_sentence,charset)
	new_trans_set = []
	for x in trans_set:
		new_trans_set.append(sentence_sim.multiple_replace(x,charset))
	
	count_box[:] = []
	for i in range(len(trans_set)):
		count_box.append([])

	for j,oc in enumerate(origin_sentence):
		for i in range(len(new_trans_set)):
			if not new_trans_set[i].find(oc)==-1:
				count_box[i].append(j) 

	start,end,score = find_max_range(count_box,origin_id)

	return start,end,score


def find_max_range(count_box,line_id):
	max_score = 0
	start = max(3*line_id-3,0)
	end = 5*line_id+3
	i =  start
	actual_start = -1
	actual_end = -1



	def find_range(count_box,raw_start):
		start_index = raw_start
		while len(count_box[start_index]) ==0:
			start_index+=1

		consecutive_empty_num = 0
		max_char_index = 0
		count = 0
		num = 0
		end_index = start_index+1
		end_type = -1
		inverse_num=0
		i = start_index
		while len(count_box[i])>0 or consecutive_empty_num<2:
			if len(count_box[i]) == 0:
				if len(count_box[i-1])==0:
					consecutive_empty_num+=1
				else:
					consecutive_empty_num=1
				if consecutive_empty_num>1:
					end_type = 1
					break
			elif max_char_index >min(count_box[i]):
				inverse_num+=1
				if inverse_num>1:
					end_type = 0
					break
			else:
				max_char_index = max(count_box[i])
		
			num+=len(count_box[i])

			i+=1
			if i == len(count_box):
				break

		if end_type == 1:
			end_index = i-1
		else:
			if len(count_box[i-1])==0:
				i-=1
			end_index = i

		return start_index,end_index, num*(end_index-start_index)

	while i<end:
		start_index,end_index,score = find_range(count_box,i)
		if max_score<score:
			max_score = score
			actual_start = start_index
			actual_end = end_index
		i = end_index

		# if line_id == 4:
		# 	print end_index,score
		# 	pdb.set_trace()

	return actual_start,actual_end,max_score




origin_set = open('D:\MSRA\dataset\\raw\\twenty_four_history\shiji\shiji_origin_split.txt','r').readlines()
trans_set = open('D:\MSRA\dataset\\raw\\twenty_four_history\shiji\shiji_trans_split.txt','r').readlines()
origin_set = map(lambda x:x.decode('utf-8').strip(),origin_set)
trans_set = map(lambda x:x.decode('utf-8').strip(),trans_set)
pairs = []
last_end = 0
end = 0
count_box = []

for jj,ors in enumerate(origin_set):
	if end >= 0:
		last_end = end
	else:
		last_not_found = True
	start,end,score = find_match_index(ors,jj,trans_set)
	print (jj,start,end,score)
	print count_box[start-1:end+1]
	if jj == 19:
		pdb.set_trace()

	# if not end == -1:
	# 	trs =''
	# 	for ii in range(start,end):
	# 		trs += trans_set[ii]
	# 	trs+='\n'
	# 	pairs.append((ors,trs))
