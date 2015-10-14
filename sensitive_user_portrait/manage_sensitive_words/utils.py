# -*- coding:utf-8 -*-

# sensitive words management
# recommend new words for lastest 7 days
# dataform: recommend_sensitive_words_date, word, [times, uids]
# include new words 

import redis
import time
import json
from elasticsearch import Elasticsearch
from sensitive_user_portrait.global_utils import R_RECOMMENTATION as r
from sensitive_user_portrait.global_utils import es_user_profile
from sensitive_user_portrait.time_utils import ts2datetime, datetime2ts

def recommend_new_words(date_list):
    results = []
    for date in date_list:
        date = date.replace('-', '')
        words_dict = r.hgetall('recommend_sensitive_words_'+date)
        if words_dict:
            for key, value in words_dict.items():
                detail = []
                detail.append(key)
                value = json.loads(value)
                uid_list = value[0]
                uname = []
                try:
                    search_results = es_user_profile.mget(index='weibo_user', doc_type='user', body={'ids': uid_list})['docs']
                    for item in search_results: 
                        if item['found']:
                            uname.append(item['_source']['nick_name'])
                        else:
                            uname.append('unknown')
                except:
                    uname = uid_list
                detail.extend([uname,value[1]])
                results.append(detail)
    sorted_results = sorted(results, key=lambda x:x[2], reverse=True)
    return sorted_results

def identify_in(date, words_list):
    # identify_in date and words_list(include level and category, [word, level, category])
    # date is date when new words were recommended
    new_list = []
    print words_list
    for item in words_list:
        r.hset('sensitive_words', item[0], json.dumps([item[1], item[2]]))
        new_list.append(item[0])
        r.hset('history_in_'+date, item[0], json.dumps([item[1], item[2]]))
    if new_list:
        for item in new_list:
            r.hdel('recommend_sensitive_words_'+date, item)
    return '1'


def search_sensitive_words(level, category): # level: 0, 1, 2, 3; category: '', or other category
    results = dict()
    word_list = []
    words_dict = r.hgetall('sensitive_words')
    if words_dict:
        if int(level) == 0 and not category:
            word_list = []
            for k,v in words_dict.items():
                word_state = json.loads(v)
                word_list.append([k, word_state[0], word_state[1]])
        elif level and category:
            word_list = []
            for k,v in words_dict.items():
                word_state = json.loads(v)
                if int(level) == int(word_state[0]) and category == word_state[1]:
                    word_list.append([k, word_state[0], word_state[1]])
        elif not level and category:
            for k,v in words_dict.items():
                word_state = json.loads(v)
                if catetory == word_state[1]:
                    word_list.append([k, word_state[0], word_state[1]])
        else:
            for k,v in words_dict.items():
                word_state = json.loads(v)
                if int(level) == int(word_state[0]):
                    word_list.append([k, word_state[0], word_state[1]])
    return word_list


def self_add_in(date, word, level, category):
    r.hset('sensitive_words', word, json.dumps([level, category]))
    r.hset('history_in_'+date, word, json.dumps([level, category]))
    return '1'

def self_delete(word):
    r.hdel('sensitive_words', word)
    r.sadd('black_sensitive_words', word)
    return '1'

def lastest_identify_in():
    results = dict()
    now_ts = time.time()
    now_ts = datetime2ts('2013-09-08')
    for i in range(1,8):
        ts = now_ts - i * 3600 *24
        date = ts2datetime(ts).replace('-','')
        words_dict = r.hgetall('history_in_'+date)
        for item in words_dict:
            results[item] = json.loads(words_dict[item])

    return results






