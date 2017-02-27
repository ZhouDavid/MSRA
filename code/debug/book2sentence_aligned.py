# -*-coding:utf-8 -*-
import sys

import para_alignment
import sentence_sim
import sentence_split

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('<usage>:<origin file path> <translation file path> <output path>.')
        exit(0)
    org_file = sys.argv[1]
    trs_file = sys.argv[2]
    out_path = sys.argv[3]
    out_org_file = out_path + '\\' + 'origin'
    out_trs_file = out_path + '\\' + 'trans'

    aligned_ors_para, aligned_trs_para = para_alignment.para_align(org_file,trs_file,out_path)

    aligned_ors_para = map(lambda x:x.encode('utf-8')+'\n',aligned_ors_para)
    aligned_trs_para = map(lambda x:x.encode('utf-8')+'\n',aligned_trs_para)

    open(out_org_file,'w').writelines(aligned_ors_para)
    open(out_trs_file,'w').writelines(aligned_trs_para)