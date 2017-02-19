# -*-coding:utf-8-*-
lines = open('shiji_trans_split.txt','r').readlines()
new_lines = []
for line in lines:
	small_lines = line.split(',')
	for i in range(len(small_lines)-1):
		small_lines[i] = small_lines[i]+'，\n'
	new_lines+=small_lines
open('shiji_trans_split2.txt','w').writelines(new_lines)