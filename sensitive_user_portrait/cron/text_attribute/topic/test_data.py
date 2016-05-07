#-*-coding=utf-8-*-
#vision2
import os
import re
import sys
import json
import csv
from config import load_scws,single_word_whitelist,black_word,cx_dict,re_cut

def input_data():#测试输入

    uid_weibo = dict()
    uid_list = []
    sw = load_scws()
    reader = csv.reader(file('./weibo_data/uid_text_0728.csv', 'rb'))
    for mid,w_text in reader:
        text = re_cut(w_text)
        if mid not in uid_list:
            uid_list.append(mid)
        if uid_weibo.has_key(mid):
            word_dict = uid_weibo[mid]
            words = sw.participle(text)
            for word in words:
                if (word[1] in cx_dict) and (3 < len(word[0]) < 30 or word[0] in single_word_whitelist) and (word[0] not in black_word):#选择分词结果的名词、动词、形容词，并去掉单个词
                    if word_dict.has_key(str(word[0])):
                        word_dict[str(word[0])] = word_dict[str(word[0])] + 1
                    else:
                        word_dict[str(word[0])] = 1
            uid_weibo[mid] = word_dict
        else:
            word_dict = dict()
            words = sw.participle(text)
            for word in words:
                if (word[1] in cx_dict) and (3 < len(word[0]) < 30 or word[0] in single_word_whitelist) and (word[0] not in black_word):#选择分词结果的名词、动词、形容词，并去掉单个词
                    if word_dict.has_key(str(word[0])):
                        word_dict[str(word[0])] = word_dict[str(word[0])] + 1
                    else:
                        word_dict[str(word[0])] = 1
            uid_weibo[mid] = word_dict
    
    return uid_list,uid_weibo
    
if __name__ == '__main__':
    input_data()
