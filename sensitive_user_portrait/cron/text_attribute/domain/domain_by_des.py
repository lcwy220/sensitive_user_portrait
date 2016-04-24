#-*-coding=utf-8-*-

import os
import re
import sys
import json
import csv
import heapq
import scws
import time
from decimal import *
from global_utils_do import txt_labels,DES_DICT,DES_COUNT,LEN_DES,TOTAL_DES,DOMAIN_P,sw,black_word,single_word_whitelist,cx_dict,black_word

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


def com_p(word_list,domain_dict,domain_count,len_dict,total):

    p = 0
    test_word = set(word_list.keys())
    train_word = set(domain_dict.keys())
    c_set = test_word & train_word
    p = sum([float(domain_dict[k]*word_list[k])/float(domain_count) for k in c_set])

    return p

def rank_dict(has_word):

    n = len(has_word)
    keyword = TopkHeap(n)
    count = Decimal(0)
    for k,v in has_word.iteritems():
        keyword.Push((v,k))
        count = count + Decimal(v)

    keyword_data = keyword.TopK()
    if count > 0:
        label = [txt_labels[txt_labels.index(keyword_data[0][1])],txt_labels[txt_labels.index(keyword_data[1][1])],txt_labels[txt_labels.index(keyword_data[2][1])]]
    else:
        label = ['other']

    return label

def domain_classify_by_des(user_weibo):#根据用户微博文本进行领域分类
    '''
    输入数据：字典
    {uid:个人简介字符串,...}
    输出数据：字典
    {uid:label1,uid2:label2,...}
    '''
    result_data = dict()
    for k,v in user_weibo.items():
        start = time.time()
        words = sw.participle(v)
        domain_p = DOMAIN_P
        word_list = dict()
        for word in words:
            if (word[1] in cx_dict) and 3 < len(word[0]) < 30 and (word[0] not in black_word) and (word[0] not in single_word_whitelist) and (word[0] not in word_list):#选择分词结果的名词、动词、形容词，并去掉单个词
                if word_list.has_key(word[0]):
                    word_list[word[0]] = word_list[word[0]] + 1
                else:
                    word_list[word[0]] = 1
        for d_k in domain_p.keys():
            domain_p[d_k] = com_p(word_list,DES_DICT[d_k],DES_COUNT[d_k],LEN_DES[d_k],TOTAL_DES)#计算文档属于每一个类的概率
            
        label = rank_dict(domain_p)
        result_data[k] = label

    return result_data



