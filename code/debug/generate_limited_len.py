# -*-coding:utf-8 -*-
import sentence_sim
charset = u'，。,：?、”“—.！!》《'
def word_len(s):
	s = sentence_sim.multiple_replace(s,charset)
	return len(s)

def find_match_sentence(origin_sentence, trans_sentences):
	count_box = [0] * len(trans_sentences)
	origin_sentence = sentence_sim.multiple_replace(origin_sentence, charset)
	for j, oc in enumerate(origin_sentence):
		for i in range(len(trans_sentences)):
			tmp_trans = sentence_sim.multiple_replace(trans_sentences[i], charset)
			if not tmp_trans.find(oc) == -1:
				count_box[i] += 1

	max_length = -1
	for i in range(len(trans_sentences)):
		if max_length < count_box[i]:
			max_length = count_box[i]
			index = i
	return index, max_length


origin_lines = open('D:\MSRA\dataset\\raw\\twenty_four_history\shiji\\shiji_origin_sentence_aligned.txt','r').readlines()
trans_lines = open('D:\MSRA\dataset\\raw\\twenty_four_history\shiji\\shiji_trans_sentence_aligned.txt','r').readlines()

origin_lines = map(lambda x:x.decode('utf-8').strip(),origin_lines)
trans_lines = map(lambda x:x.decode('utf-8').strip(),trans_lines)

max_length = 50
count = 0
new_or = []
new_tr = []
print len(origin_lines)
print len(trans_lines)
for i in range(len(origin_lines)):
	if i%10000 ==0:
		print i
	if word_len(origin_lines[i])<=max_length and word_len(trans_lines[i])<=max_length:
		new_or.append(origin_lines[i])
		new_tr.append(trans_lines[i])
	else:
		tmp_ors = origin_lines[i].split(u'，')
		tmp_trs = trans_lines[i].split(u'，')
		for j,o in enumerate(tmp_ors):
			if word_len(o)<max_length and word_len(o)>3:
				index,score = find_match_sentence(o,tmp_trs)
				if score>3 and word_len(tmp_trs[index])<max_length:
					if j<len(tmp_ors)-1:
						new_or.append(o+u'，')
						new_tr.append(tmp_trs[index]+u'，')
					else:
						new_or.append(o)
						new_tr.append(tmp_trs[index])

new_or = map(lambda x:x.encode('utf-8')+'\n',new_or)
new_tr = map(lambda x:x.encode('utf-8')+'\n',new_tr)

open('D:\MSRA\dataset\\raw\\twenty_four_history\shiji\\shiji_origin_max_length_30.txt','w').writelines(new_or)
open('D:\MSRA\dataset\\raw\\twenty_four_history\shiji\\shiji_trans_max_length_30.txt','w').writelines(new_tr)
