# -*- coding: UTF-8 -*-
import gensim
from gensim import corpora, models, similarities
import time
import datetime
import csv
import heapq
from operator import itemgetter, attrgetter
from lda_config import re_cut,WORD_N,WHOLE_WORD,MAX_NT,MIN_NT,STA_COUNT
from textrank4zh import TextRank4Keyword, TextRank4Sentence
#from test_data import input_data

tr4w = TextRank4Keyword()

class TopkHeap(object):
    def __init__(self, k):
        self.k = k
        self.data = []
 
    def Push(self, elem):
        if len(self.data) < self.k:
            heapq.heappush(self.data, elem)
        else:
            topk_small = self.data[0][0]
            if elem[0] > topk_small:
                heapq.heapreplace(self.data, elem)
 
    def TopK(self):
        return [x for x in reversed([heapq.heappop(self.data) for x in xrange(len(self.data))])]

def get_data(weibo):#分词

    uid_word = []
    text_str = ''
    for text in weibo:
        if isinstance(text,unicode):
            text = text.encode('utf-8')
        else:
            text = text
        v = re_cut(text)
        text_str = text_str + v + '。'
        word_list = get_keyword(v)
        uid_word.append(word_list)

    word_whole = get_keyword_whole(text_str)

    return uid_word,word_whole

def get_keyword(text):

    tr4w.analyze(text=text, lower=True, window=2)
    k_dict = tr4w.get_keywords(WORD_N, word_min_len=2)
    word_list = []
    for item in k_dict:
        word_list.append(item.word.encode('utf-8'))

    return word_list

def get_keyword_whole(text):

    tr4w.analyze(text=text, lower=True, window=2)
    k_dict = tr4w.get_keywords(WHOLE_WORD, word_min_len=2)
    word_list = dict()
    for item in k_dict:
        word_list[item.word.encode('utf-8')] = item.weight

    return word_list

def lda_main(texts,nt,word_whole):
    '''
        lda方法主函数：
        输入数据：
        texts：list对象，一条记录表示一个用户发布
    '''

    ##生成字典
    dictionary=corpora.Dictionary(texts)
    dictionary.filter_extremes(no_below=5, no_above=0.5, keep_n=None)
    corpus = [dictionary.doc2bow(text) for text in texts]

    ##生成tf-idf矩阵
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    ##LDA模型训练
    lda = gensim.models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=nt, update_every=1, chunksize=5000, passes=1)

    ##将对应的topic写入文件
    topics=lda.show_topics(num_topics=nt, num_words=10, log=False, formatted=True)
    
    keyword = TopkHeap(nt)
    for t in topics:
        word_list = t[1].encode('utf-8')
        item=''.join(word_list.split())
        w_item=item.split('+')
        weight_t = 0
        for i in w_item:
            w,c=i.split('*')
            try:
                weight_t = weight_t + word_whole[c]
            except:
                continue
        keyword.Push((weight_t,item))

    keyword_data = keyword.TopK()

    return keyword_data

def topic_lda_main(weibo):
    '''
        主函数：
        输入数据：微博list
        输出数据：话题list
        输出示例：
        [[weight1,topic1],[weight2,topic2]...]
    '''
    n = len(weibo)
    c_n = n/STA_COUNT
    if c_n > MAX_NT:
        nt = MAX_NT
    elif c_n < MIN_NT:
        nt = MIN_NT
    else:
        nt = c_n
    
    texts,word_whole = get_data(weibo)
    topics = lda_main(texts,nt,word_whole)

    return topics


if __name__ == '__main__':

    weibo = input_data()
    start = time.time()
    topics = topic_lda_main(weibo)
    end = time.time()
    print 'it takes %s seconds...' % (end-start)

    f=open('./weibo_data/weibo_topic2.txt','w')
    for t in topics:
        f.write(str(t[0])+'\t'+t[1]+'\n')

