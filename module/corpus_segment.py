from __future__ import unicode_literals
import codecs
import re

re_han_cut = re.compile("([\u4E00-\u9FD5a-zA-Z0-9-+#&\._/\u03bc\u3001\(\)\uff08\uff09\~\'\u2019]+)",re.U)
re_han= re.compile("([\u4E00-\u9FD5]+)",re.U)


class Cuting(object):

    def __init__(self,file_corpus,file_dict,file_segment):
        self.file_corpus =file_corpus
        self.file_dict =file_dict
        self.file_segment =file_segment
        self.wdict={}
        self.get_dict()

    def get_dict(self):
        f=codecs.open(self.file_dict,'r',encoding='utf-8')
        for lineno,line in enumerate(f,1):
            line=line.strip()
            line=line.split('\t')
            w=line[0]
            if w :
                if w[0] in self.wdict:
                    value = self.wdict[w[0]]
                    value.append(w)
                    self.wdict[w[0]] = value
                else:
                    self.wdict[w[0]] = [w]

    def fmm(self, sentence):
        N = len(sentence)
        k = 0
        result = []
        while k < N:
            w = sentence[k]
            maxlen = 1
            if w in self.wdict:
                words = self.wdict[w]
                t = ''
                for item in words:
                    itemlen = len(item)
                    if sentence[k:k + itemlen] == item and itemlen >= maxlen:
                        t = item
                        maxlen = itemlen
                if t and t not in result:
                    result.append(t)
            k = k + maxlen
        return result

    def judge(self,words):
        flag = False
        n = len(''.join(re_han.findall(words)))
        if n == len(words):
            flag = True
        return flag

    def cut(self,sentence):
        buf=[]
        blocks = re_han_cut.findall(sentence)
        for blk in blocks:
            if blk:
                fm=self.fmm(blk)
                if fm:
                    try:
                        re_split=re.compile('|'.join(fm))
                        for s in re_split.split(blk):
                            if s and self.judge(s):
                                buf.append(s)
                    except:
                        pass

        return buf

    def find(self):
        input_data=codecs.open(self.file_corpus,'r',encoding='utf-8')
        output_data=codecs.open(self.file_segment,'w',encoding='utf-8')
        dataset={}
        for lineno,line in enumerate(input_data,1):
            line=line.strip()
            for w in self.cut(line):
                if len(w)>=2:
                    dataset[w]=dataset.get(w,0)+1
        data_two=sorted(dataset.items(), key=lambda d: d[1], reverse=True)
        seg_num=len(data_two)
        for key in data_two:
            output_data.write(key[0]+'\t'+str(key[1])+'\n')

        print('Having segment %d words'%seg_num)
        input_data.close()
        output_data.close()

        return seg_num