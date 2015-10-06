# -*- coding:utf-8 -*-

# sensitive words management
# recommend new words for lastest 7 days
# dataform: recommend_sensitive_words_date, word, [times, uids]
# include new words 

import redis
import json
from sensitive_user_portrait.global_utils import R_RECOMMENTATION as r
from sensitive_user_portrait.time_utils import ts2datetime, datetime2ts

def recommend_new_words(date_list):
    results = dict()
    for date in date_list:
        date = date.replace('-', '')
        words_dict = r.hgetall('recommend_sensitive_words_'+date)
        if words_dict:
            words_dict = json.loads(words_dict)
            results[date] = words_dict
    return results

def identify_in(date, words_list):
    # identify_in date and words_list(include level and category, [word, level, category])
    # date is date when new words were recommended
    new_dict = dict()
    for item in words_list:
        r.hset('sensitive_words', item[0], json.dumps([item[1], item[2]]))
        new_dict[item[0]] = json.dumps([item[1], item[2]])
    history_in_list = r.hget('history_in_'+date)
    history_in_dict = {}
    if history_in_list:
        history_in_dict = json.loads(history_in_list)
    history_in_dict.update(new_dict)
    for item in history_in_dict:
        r.hset('history_in_'+date, item, history_in_dict[item])
    if new_list:
        for item in new_list:
            r.hdel('recommend_sensitive_words_'+date, item)
    return '1'


def search_sensitive_words(state):
    results = dict()
    words_list = []
    words_dict = r.hgetall('sensitive_words')
    if words_dict:
        if state == "level":
            for k,v in words_dict.items():
                word_state = json.loads(v)
                level_1 = []
                level_2 = []
                level_3 = []
                if word_state[0] == '1':
                    level_1.append(k)
                elif word_state[0] == "2":
                    level_2.append(k)
                else:
                    level_3.append(k)
            results['level_1'] = level_1
            results['level_2'] = level_2
            results['level_3'] = level_3
        elif state == "category":
            for k,v in words_dict.items():
                word_state = json.loads(v)
                try:
                    results[v[1]].append(k)
                else:
                    results[v[1]] = [k]
        else:
            pass

    return results

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






