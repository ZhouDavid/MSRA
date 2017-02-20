#-*-coding:utf-8 -*-

charset = u'，。,：?、”“—.！!》《\n'
import sentence_sim
import pdb

#origin_sentence
def find_match_index(origin_sentence,origin_id,trans_set,last_end,last_not_found):
	start = -1
	end = -1
	origin_sentence = sentence_sim.multiple_replace(origin_sentence,charset)
	new_trans_set = []
	for x in trans_set:
		new_trans_set.append(sentence_sim.multiple_replace(x,charset))
	
	count_box = []
	for i in range(len(trans_set)):
		count_box.append([])

	for j,oc in enumerate(origin_sentence):
		for i in range(len(new_trans_set)):
			if not new_trans_set[i].find(oc)==-1:
				count_box[i].append(j) 

	start,end = find_max_range(count_box,origin_id,last_end,last_not_found)

	return start,end

# def find_range(count_box,start_index):
# 	i = start_index
# 	consecutive_empty_num = 0
# 	max_char_index = 0
# 	count = 0
# 	num = 0
# 	end_index = start_index+1
# 	while (len(count_box[i])>0 and max_char_index<max(count_box[i])) or consecutive_empty_num<2:
# 		if len(count_box[i]) == 0:
# 			consecutive_empty_num+=1
# 		else:
# 			max_char_index = max(count_box[i])
# 			end_index = i+1
	
# 		count+=1
# 		num+=len(count_box[i])

# 		i+=1
# 		if i == len(count_box):
# 			break
# 	return end_index,count*num


def find_max_range(count_box,line_id,last_end,last_not_found):
	max_score = 0
	start = last_end
	end = -1
	i = last_end  #偏置
	not_found_num = 0
	eof_index = min(line_id*6,len(count_box))
	while len(count_box[i])==0:
		i+=1

	def find_range(count_box,start_index):
		i = start_index
		consecutive_empty_num = 0
		max_char_index = 0
		count = 0
		num = 0
		end_index = start_index+1
		while (len(count_box[i])>0 and max_char_index<=min(count_box[i])) or consecutive_empty_num<2:
			if len(count_box[i]) == 0:
				consecutive_empty_num+=1
				if consecutive_empty_num>1:
					break
			else:
				max_char_index = max(count_box[i])
		
			count+=1
			num+=len(count_box[i])

			i+=1
			if i == len(count_box):
				break
		end_index = i
		return end_index,count*num
	# full_stop_num=0
	# while i < eof_index:
	# 	if len(count_box[i]) > 0:
	# 		score = 0
	# 		length = 0
	# 		num = len(count_box[i])
	# 		j=i+1
	# 		while j<end_index and not_found_num<=1:
	# 			if len(count_box[j]) == 0:
	# 				if len(trans_set[j])>10:
	# 					break
	# 				else:
	# 					not_found_num+=1
	# 			if not_found_num>1:
	# 				j-=1
	# 				break
	# 			if len(count_box[j])>0:
	# 				pdb.set_trace()
	# 				if max(count_box[j-1])>max(count_box[j]):
	# 					break
	# 			if trans_set[j-1].endswith(u'。'):
	# 				full_stop_num+=1

	# 			if full_stop_num>1:
	# 				j+=1
	# 				break

	# 			num += len(count_box[j])
	# 			j+=1

	# 		length = j-i
	# 		score = num*length
	# 		if max_score<score:
	# 				max_score = score
	# 				start = i
	# 				end = j
	# 		i = j
		
	# 	else:
	# 		i+=1
	while i<eof_index:
		end_index,score = find_range(count_box,i)
		if max_score<score:
			max_score = score
			start = i
			end = end_index
		i = end_index
		if line_id == 4:
			pdb.set_trace()

	return start,end






origin_set = open('E:\MSRA\dataset\\raw\\twenty_four_history\shiji\shiji_origin_split.txt','r').readlines()
trans_set = open('E:\MSRA\dataset\\raw\\twenty_four_history\shiji\shiji_trans_split2.txt','r').readlines()
origin_set = map(lambda x:x.decode('utf-8').strip(),origin_set)
trans_set = map(lambda x:x.decode('utf-8').strip(),trans_set)
pairs = []
last_end = 0
end = 0
last_not_found = False

for jj,ors in enumerate(origin_set):
	if end >= 0:
		last_end = end
	else:
		last_not_found = True
	start,end = find_match_index(ors,jj+1,trans_set,last_end,last_not_found)
	print (jj,start,end)

	if not end == -1:
		trs =''
		for ii in range(start,end):
			trs += trans_set[ii]
		trs+='\n'
		pairs.append((ors,trs))
