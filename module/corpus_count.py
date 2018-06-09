from __future__ import unicode_literals
import  re
import codecs
import json

re_han = re.compile("([\u4E00-\u9FD5a-zA-Z0-9-+#&\._/\u03bc\u3001\(\)\uff08\uff09\~\'\u2019]+)",re.U)

class Finding(object):

    def __init__(self,file_corpus,file_count,count):
        self.file_corpus=file_corpus
        self.file_count=file_count
        self.count=count

    def split_text(self,sentence):
        seglist = re_han.findall(sentence)
        return seglist

    def count_word(self,seglist,k):
        for words in seglist:
            ln=len(words)
            i=0
            j=0
            if words:
                while 1:
                    j = i + k
                    if j<=ln:
                        word=words[i:j]
                        if i==0:
                            lword='S'
                        else:
                            lword=words[i-1:i]
                        if j==ln:
                            rword='E'
                        else:
                            rword=words[j:j+1]
                        i+=1
                        yield word,lword,rword
                    else:
                        break

    def find_word(self):
        input_data = codecs.open(self.file_corpus, 'r', encoding='utf-8')
        dataset = {}
        for lineno, line in enumerate(input_data, 1):
            try:
                line = line.strip()
                seglist = self.split_text(line)
                for w, lw, rw in self.count_word(seglist, self.count):
                    if w not in dataset:
                        dataset.setdefault(w, [[], {}, {}])
                        dataset[w][0] = 1
                    else:
                        dataset[w][0] += 1
                    if lw:
                        dataset[w][1][lw] = dataset[w][1].get(lw, 0) + 1
                    if rw:
                        dataset[w][2][rw] = dataset[w][2].get(rw, 0) + 1

            except:
                pass
        self.write_data(dataset)

    def write_data(self,dataset):
        output_data = codecs.open(self.file_count, 'w', encoding='utf-8')
        for word in dataset:
            output_data.write(word+'\t'+json.dumps(dataset[word], ensure_ascii=False, sort_keys=False)+'\n')
        output_data.close()

