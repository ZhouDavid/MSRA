#-*-coding:utf-8 -*-
lines = open(u'白话二十四史之18【宋史（下）、辽史.txt','r').readlines()
liao = lines[10014:len(lines)]
songxia = lines[0:10014]
open('songshixia.txt','w').writelines(songxia)
open('liaoshi.txt','w').writelines(liao)
