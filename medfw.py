from __future__ import absolute_import
__version__ = '1.0'
__license__ = 'MIT'

import os
import re
import logging
import time
import codecs

from module._compat import *
from module.corpus_count import *
from module.corpus_segment import *
from module.select_model import *
from module.words_search import *



medfw_path=os.getcwd()
file_corpus=medfw_path+'/data/file_corpus.txt'
file_dict=medfw_path+'/data/dict.txt'
file_count_one=medfw_path+'/data/count_one.txt'
file_count_two=medfw_path+'/data/count_two.txt'
file_segment=medfw_path+'/data/file_segment.txt'


log_console = logging.StreamHandler(sys.stderr)
default_logger = logging.getLogger(__name__)
default_logger.setLevel(logging.DEBUG)
default_logger.addHandler(log_console)

def setLogLevel(log_level):
    global logger
    default_logger.setLevel(log_level)


class MedFW(object):
    def __init__(self,K=10.8,H=0.1,R=60,Y=5000):
        self.K=K  #parameter of PMI to select stable words in step2
        self.H=H  #paramteter of top H segment words to search engine in step4
        self.R=R  #parameter of over the frequency of segment words in search engine to add dict in step4
        self.Y=Y  #parameter of the conditions for ending the iteration
        self.seg_num=0

    #step1: count corpus
    def medfw_s1(self):
        for i in range(1,3):
            if i==1:
                file_count=file_count_one
            else:
                file_count=file_count_two
            default_logger.debug("Counting courpus to get %s...\n" % (file_count))
            t1 = time.time()
            cc=Finding(file_corpus,file_count,i)
            cc.find_word()
            default_logger.debug("Getting %s cost %.3f seconds...\n" % (file_count,time.time() - t1))

    #step2: select stable words and  generate initial vocabulary
    def medfw_s2(self):
        default_logger.debug("Select stable words and  generate initial vocabulary... \n")
        select(file_count_one,file_count_two,file_dict,self.K)

    #step3: use initial vocabulary to segment corpus
    def medfw_s3(self):
        t1 = time.time()
        sc=Cuting(file_corpus,file_dict,file_segment)
        self.seg_num=sc.find()
        default_logger.debug("Segment corpus cost %.3f seconds...\n" % (time.time() - t1))

    #step4:use search engine to select words of segment corpus
    def medfw_s4(self,H,R,iternum):
        t1 = time.time()
        search(file_segment,file_dict,H,R,iternum)
        default_logger.debug("Segment corpus cost %.3f seconds...\n" % (time.time() - t1))

    def medfw(self):
        # default_logger.debug("Starting to find words and do step1...\n" )
        print('-----------------------------------')
        print('step1:count corpus')
        self.medfw_s1()

        print('-----------------------------------')
        print('step2:select stable words and  generate initial vocabulary')
        self.medfw_s2()

        print('-----------------------------------')
        print('step3:use initial vocabulary to segment corpus')
        self.medfw_s3()

        print('-----------------------------------')
        print('step4:use search engine to select words of segment corpus')
        self.medfw_s4(H=0.1,R=60,iternum=0)


        print('-----------------------------------')
        print('step5:cycling iteration')
        iter_num=1
        while True:
            default_logger.debug("Itering %d...\n" % (iter_num))
            t1 = time.time()
            self.medfw_s3()
            if self.seg_num<self.Y:
                self.medfw_s4(H=1,R=60,iternum=iter_num)
                default_logger.debug("Ending the iteration ...\n")
                break
            else:
                self.medfw_s4(H=0.1,R=60,iternum=iter_num)
                iter_num+=1
            default_logger.debug("Itering %d cost %.3f seconds...\n " % ((iter_num-1), time.time() - t1))

        with codecs.open(file_dict, 'r', encoding='utf-8') as f:
            total_num=len(f.readlines())

        print('Having succcessfuly find %d words from corpus '%total_num)





if __name__ == '__main__':
    md=MedFW(K=10.8,H=0.1,R=60,Y=5000)
    md.medfw()