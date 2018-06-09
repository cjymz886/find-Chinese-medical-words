#encoding:utf-8

import codecs
import json
import math


def load_data(file_count_one):
    count_one_data=codecs.open(file_count_one,'r',encoding='utf-8')
    count_one_param={}
    N=0
    for line in count_one_data.readlines():
        line=line.strip()
        line=line.split('\t')
        try:
            word=line[0]
            value=json.loads(line[1])
            N += value[0]
            count_one_param[word]=int(value[0])
        except:
            pass
    count_one_data.close()

    return N,count_one_param

def select(file_count_one,file_count_two,file_dict,K=10.8):

    count_two_data=codecs.open(file_count_two,'r',encoding='utf-8')
    N,count_one_param=load_data(file_count_one)
    count_two_param={}

    for line in count_two_data.readlines():
        line=line.strip()
        line=line.split('\t')
        try:
            word=line[0]
            value=json.loads(line[1])
            P_w=1.0*value[0]/N
            P_w1=1.0*count_one_param.get(word[0],1)/N
            P_w2=1.0*count_one_param.get(word[1],1)/N
            mi=math.log(P_w/(P_w1*P_w2))
            count_two_param[word]=mi
        except:
            pass
    select_two_param=[]
    for w in count_two_param:
        mi=count_two_param[w]
        if mi>K:
            select_two_param.append(w)

    with codecs.open(file_dict,'a',encoding='utf-8') as f:
        for w in select_two_param:
            f.write(w+'\t'+'org'+'\n')

    count_two_data.close()

