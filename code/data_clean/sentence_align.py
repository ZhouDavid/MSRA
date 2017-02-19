#-*-coding:utf-8 -*-

charset = u'，。,：?、”“—.！!》《\n'
import sentence_sim
import pdb

origin_sentence
def find_match_index(origin_sentence,origin_id,trans_set,last_end,last_not_found):
	start = -1
	end = -1
	origin_sentence = sentence_sim.multiple_replace(origin_sentence,charset)
	new_trans_set = []
	for x in trans_set:
		new_trans_set.append(sentence_sim.multiple_replace(x,charset))
	

	count_box = [0]*len(new_trans_set)
	for oc in origin_sentence:
		for i in range(len(new_trans_set)):
			if not new_trans_set[i].find(oc)==-1:
				count_box[i]+=1

	start,end = find_max_range(count_box,origin_id,last_end,last_not_found)



	return start,end

def find_max_range(count_box,line_id,last_end,last_not_found):
	max_score = 0
	start = last_end
	end = -1
	i = last_end  #偏置
	not_found_num = 0
	end_index = min(line_id*6,len(count_box))
	while count_box[i]==0:
		i+=1
	full_stop_num=0
	while i < end_index:
		if count_box[i] > 0:
			score = 0
			length = 0
			num = count_box[i]
			j=i
			while j<end_index and count_box[j]>0:
				j+=1
				if trans_set[j].endswith(u'。'):
					full_stop_num+=1
				if full_stop_num>1:
					j+=1
					break
				num+=count_box[j]

			length = j-i
			score = num*length
			if max_score<score:
					max_score = score
					start = i
					end = j
			i = j
		else:
			if len(trans_set[i])<=5:
				not_found_num+=1
				if not_found_num >1:
					break
			else:
				break
		i+=1
	#pdb.set_trace()
	return start,end






origin_set = open('D:\MSRA\dataset\\raw\\twenty_four_history\shiji\shiji_origin_split.txt','r').readlines()
trans_set = open('D:\MSRA\dataset\\raw\\twenty_four_history\shiji\shiji_trans_split2.txt','r').readlines()
origin_set = map(lambda x:x.decode('utf-8').strip(),origin_set)
trans_set = map(lambda x:x.decode('utf-8').strip(),trans_set)
pairs = []
last_end = 0
end = 0
last_not_found = False

for j,ors in enumerate(origin_set):
	if end >= 0:
		last_end = end
	else:
		last_not_found = True
	start,end = find_match_index(ors,j+1,trans_set,last_end,last_not_found)
	print (j,start,end)
	#pdb.set_trace()
	if not start == -1:
		trs =''
		for i in range(start,end):
			trs += trans_set[i]
		trs+='\n'
		pairs.append((ors,trs))
