#encoding:utf-8
import requests
from lxml import etree
import codecs
import re


def search(file_segment,file_dict,H,R,iternum):
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, sdch, b',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.'
               }

    input_data=codecs.open(file_segment,'r',encoding='utf-8')
    read_data=input_data.readlines()
    N=int(len(read_data)*H)
    output_data=codecs.open(file_dict,'a',encoding='utf-8')
    n=1
    m=1
    for line in read_data[:N]:
        line=line.rstrip()
        line=line.split('\t')
        word=line[0]
        try:
            urlbase = 'https://www.baidu.com/s?wd=' + word
            dom = requests.get(urlbase, headers=headers)
            ct = dom.text
            num = ct.count(word)
            html = dom.content
            selector = etree.HTML(html)
            flag = False
            if selector.xpath('//h3[@class="t c-gap-bottom-small"]'):
                ct = ''.join(selector.xpath('//h3[@class="t c-gap-bottom-small"]//text()'))
                lable = re.findall(u'(.*)_百度百科', ct)
                for w in lable:
                    w = w.strip()
                    if w == word:
                        flag = True
            if flag:
                output_data.write(word + '\titer_'+str(iternum)+ '\n')
                n+=1
            else:
                if num >=R:
                    output_data.write(word + '\titer_' + str(iternum) + '\n')
                    n+=1
            m+=1
            if m%100==0:
                print('having crawl %dth word\n'%m)
        except:
            pass
    print('Having add %d words to file_dict at iter_%d'%(n,iternum))
    input_data.close()
    output_data.close()