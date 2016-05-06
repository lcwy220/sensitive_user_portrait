# -*- coding: utf-8 -*-

import os
import re
import scws
import sys
import csv

sys.path.append('../../../')
from parameter import DOMAIN_ABS_PATH as abs_path
from time_utils_ys import get_db_num
from global_utils_ys import es_user_profile,es_retweet,profile_index_name,\
                         profile_index_type,retweet_index_name_pre,retweet_index_type

##加载领域标签

labels = ['writer', 'professor', 'root', 'religion', 'lawyer', 'well-known', \
          'non-public', 'media', 'official-media', 'governer', 'star', 'other', 'welfare']
zh_labels = ['作家写手', '专家学者', '草根红人', '宗教人士', '维权律师', '公知分子', '非公企业主', \
             '独立媒体', '官方媒体', '公职人员', '文体明星', '其他', '社会公益']
txt_labels = ['writer', 'professor', 'root', 'religion', 'lawyer', 'well-known', \
          'non-public', 'media', 'official-media', 'governer', 'star', 'welfare']

##领域标签加载结束

##加载领域词典

def load_train():

    domain_dict = dict()
    domain_count = dict()
    for i in txt_labels:
        reader = csv.reader(file(abs_path+'/topic_dict/%s_tfidf.csv'% i, 'rb'))
        word_dict = dict()
        count = 0
        for f,w_text in reader:
            f = f.strip('\xef\xbb\xbf')
            word_dict[str(w_text)] = float(f)
            count = count + float(f)
        domain_dict[i] = word_dict
        domain_count[i] = count

    len_dict = dict()
    total = 0
    for k,v in domain_dict.items():
        len_dict[k] = len(v)
        total = total + len(v)
    
    return domain_dict,domain_count,len_dict,total

DOMAIN_DICT,DOMAIN_COUNT,LEN_DICT,TOTAL = load_train()

def load_des_train():

    domain_dict = dict()
    domain_count = dict()
    for i in txt_labels:
        reader = csv.reader(file(abs_path+'/topic_dict/%s_des.csv'% i, 'rb'))
        word_dict = dict()
        count = 0
        for f,w_text in reader:
            f = f.strip('\xef\xbb\xbf')
            word_dict[str(w_text)] = float(f)
            count = count + float(f)
        domain_dict[i] = word_dict
        domain_count[i] = count

    len_dict = dict()
    total = 0
    for k,v in domain_dict.items():
        len_dict[k] = len(v)
        total = total + len(v)
    
    return domain_dict,domain_count,len_dict,total

DES_DICT,DES_COUNT,LEN_DES,TOTAL_DES = load_des_train()

##加载领域词典结束

##加载种子用户

def readTrainUser():

    data = dict()
    for i in range(0,len(txt_labels)):
        f = open(abs_path+"/user_seed/%s.txt" % txt_labels[i],"r")
        item = []
        for line in f:
            line = line.strip('\r\n')
            item.append(line)
        data[txt_labels[i]] = set(item)
        f.close()

    return data

train_users = readTrainUser()

##加载种子用户结束

##对微博文本进行预处理

def cut_filter(text):
    pattern_list = [r'\（分享自 .*\）', r'http://\w*']
    for i in pattern_list:
        p = re.compile(i)
        text = p.sub('', text)
    return text

def re_cut(w_text):#根据一些规则把无关内容过滤掉
    
    w_text = cut_filter(w_text)
    w_text = re.sub(r'[a-zA-z]','',w_text)
    a1 = re.compile(r'\[.*?\]' )
    w_text = a1.sub('',w_text)
    a1 = re.compile(r'回复' )
    w_text = a1.sub('',w_text)
    a1 = re.compile(r'\@.*?\:' )
    w_text = a1.sub('',w_text)
    a1 = re.compile(r'\@.*?\s' )
    w_text = a1.sub('',w_text)
    if w_text == u'转发微博':
        w_text = ''

    return w_text

##微博文本预处理结束

## 加载分词工具

SCWS_ENCODING = 'utf-8'
SCWS_RULES = '/usr/local/scws/etc/rules.utf8.ini'
CHS_DICT_PATH = '/usr/local/scws/etc/dict.utf8.xdb'
CHT_DICT_PATH = '/usr/local/scws/etc/dict_cht.utf8.xdb'
IGNORE_PUNCTUATION = 1

ABSOLUTE_DICT_PATH = os.path.abspath(os.path.join(abs_path, './dict'))
CUSTOM_DICT_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'userdic.txt')
EXTRA_STOPWORD_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'stopword.txt')
EXTRA_EMOTIONWORD_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'emotionlist.txt')
EXTRA_ONE_WORD_WHITE_LIST_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'one_word_white_list.txt')
EXTRA_BLACK_LIST_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'black.txt')

cx_dict = ['an','Ng','n','nr','ns','nt','nz','vn','@']#关键词词性词典

def load_one_words():
    one_words = [line.strip('\r\n') for line in file(EXTRA_EMOTIONWORD_PATH)]
    return one_words

def load_black_words():
    one_words = [line.strip('\r\n') for line in file(EXTRA_BLACK_LIST_PATH)]
    return one_words

single_word_whitelist = set(load_one_words())
black_word = set(load_black_words())

def load_scws():
    s = scws.Scws()
    s.set_charset(SCWS_ENCODING)

    s.set_dict(CHS_DICT_PATH, scws.XDICT_MEM)
    s.add_dict(CHT_DICT_PATH, scws.XDICT_MEM)
    s.add_dict(CUSTOM_DICT_PATH, scws.XDICT_TXT)

    # 把停用词全部拆成单字，再过滤掉单字，以达到去除停用词的目的
    s.add_dict(EXTRA_STOPWORD_PATH, scws.XDICT_TXT)
    # 即基于表情表对表情进行分词，必要的时候在返回结果处或后剔除
    s.add_dict(EXTRA_EMOTIONWORD_PATH, scws.XDICT_TXT)

    s.set_rules(SCWS_RULES)
    s.set_ignore(IGNORE_PUNCTUATION)
    return s

def cut(s, text, f=None, cx=False):
    if f:
        tks = [token for token
               in s.participle(cut_filter(text))
               if token[1] in f and (3 < len(token[0]) < 30 or token[0] in single_word_whitelist)]
    else:
        tks = [token for token
               in s.participle(cut_filter(text))
               if 3 < len(token[0]) < 30 or token[0] in single_word_whitelist]
    if cx:
        return tks
    else:
        return [tk[0] for tk in tks]

sw = load_scws()
##加载分词工具结束

##标准化领域字典
def start_p():

    domain_p = dict()
    for name in txt_labels:
        domain_p[name] = 0

    return domain_p

DOMAIN_P = start_p()
##标准化结束
