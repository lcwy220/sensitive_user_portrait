# -*-coding:utf-8 -*-

import sys
import re
import csv
import json
import time
from elasticsearch import Elasticsearch
from weibo_api import read_user_weibo
from DFA_filter import sensitive_words_extract
from attribute_from_flow import get_flow_information
from user_profile import get_profile_information
from save_utils import save_user_results
from evaluate_index import get_evaluate_index

reload(sys)
sys.path.append('./../../')
from global_utils import R_RECOMMENTATION as r
from global_utils import es_sensitive_user_portrait as es
from time_utils import datetime2ts, ts2datetime

reload(sys)
sys.path.append('../../../../../libsvm-3.17/python/')
from sta_ad import load_scws

EXTRA_WORD_WHITE_LIST_PATH = './one_word_white_list.txt'
sw = load_scws()

cx_dict = ['a', 'n', 'nr', 'ns', 'nz', 'v', '@', 'd']

def load_one_words(): # one word emotion word
    one_words = [line.strip('\r\n') for line in file(EXTRA_WORD_WHITE_LIST_PATH)]
    return one_words

single_word_whitelist = set(load_one_words())
single_word_whitelist |= set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')

BLACK_WORDS_PATH = './black.txt' # filter word
def load_black_words():
    black_words = set([line.strip('\r\n') for line in file(BLACK_WORDS_PATH)])
    return black_words

black_words = load_black_words()

def get_emoticon_dict(): # enotion icons, [flower:1]
    results = dict()
    f = open('./emoticons.txt','rb')
    for line in f:
        line_list = line.split(':')
        emoticon = line_list[0]
        emo_class = line_list[1]
        try:
            results[emo_class].append(emoticon.decode('utf-8'))
        except:
            results[emo_class] = [emoticon.decode('utf-8')]
    return results

emoticon_dict = get_emoticon_dict()

def get_liwc_dict(): #angry words, [128: angry]
    results = {}
    f = open('./extract_word.csv', 'rb')
    reader = csv.reader(f)
    for line in reader:
        num = line[0]
        word = line[1]
        try:
            results[num].append(word)
        except:
            results[num] = [word]
    return results

liwc_dict = get_liwc_dict()

def attr_text_len(weibo_list): # total weibo list
    len_list = [len(weibo['text']) for weibo in weibo_list]
    if len(len_list):
        ave_len = float(sum(len_list)) / len(len_list)
    else:
        ave_len = 0
    return ave_len

def attr_emoticon(weibo_list): # total weibo list, count emotion icons
    results = {}
    for weibo in weibo_list:
        text = weibo['text']
        for emo_class in emoticon_dict:
            emoticons = emoticon_dict[emo_class]
            for emoticon in emoticons:
                if isinstance(text, str):
                    text = text.decode('utf-8')
                count = text.count(emoticon)
                if count != 0:
                    try:
                        results[emoticon] += count
                    except:
                        results[emoticon] = count

    return results

def attr_liwc(weibo_list):
    results = {}
    keyword_results = {}
    for weibo in weibo_list:
        text = weibo['text']
        cut_text = sw.participle(text.encode('utf-8'))
        cut_word_list = [term for term, cx in cut_text if cx in cx_dict]
        for num in liwc_dict:
            for liwc_word in liwc_dict[num]:
                if liwc_word in cut_word_list:
                    if num in results:
                        try:
                            results[num][liwc_word.decode('utf-8')] += 1
                        except:
                            results[num][liwc_word.decode('utf-8')] = 1
                    else:
                        results[num] = {liwc_word.decode('utf-8'): 1}

    return results

def attr_link(weibo_list):
    if len(weibo_list) == 0:
        return 0
    count = []
    for weibo in weibo_list:
        text = weibo['text']
        pat = re.compile('http://')
        urls = re.findall(pat, text)
        if len(urls):
            count.append(len(urls))
    if count:
        all_count = sum(count)
        ave_count = float(all_count) / len(weibo_list)
        return ave_count
    else:
        return 0

def attr_online_pattern(weibo_list):
    results = {}
    for weibo in weibo_list:
        online_pattern = weibo['online_pattern']
        try:
            results[online_pattern] += 1
        except:
            results[online_pattern] = 1
    return results

def attr_keywords(weibo_list):
    results = {}
    for weibo in weibo_list:
        text = weibo['text'].encode('utf-8')
        pattern_list = [r'\（分享自 .*\）', r'http://t.cn/\w*']
        for i in pattern_list:
            p = re.compile(i)
            text = p.sub('', text)

    tks = []
    for token in sw.participle(text):
        if 3<len(token[0])<30 or token[0].decode('utf-8') in single_word_whitelist:
            if token[1] in cx_dict:
                if (token[0] not in black_words):
                    tks.append(token)
                else:
                    #print 'delete:', token[0]
                    pass

    for tk in tks:
        word = tk[0].decode('utf-8')
        try:
            results[word] += 1
        except:
            results[word] = 1
    sort_results = sorted(results.items(), key=lambda x:[1], reverse=True)[:50]
    keywords_results = {}
    for sort_item in sort_results:
        keywords_results[sort_item[0]] = sort_item[1]

    return keywords_results

def attri_sensitive_words(weibo_list):
    sw_results = {}
    for item in weibo_list:
        text = item['text']
        if not isinstance(text, str):
            text = text.encode('utf-8', 'ignore')
        sw_dict = sensitive_words_extract(text)
        if not sw_dict:
            continue
        for key in sw_dict.keys():
            if sw_results.has_key(key):
                sw_results[key] += sw_dict[key]
            else:
                sw_results[key] = sw_dict[key]
    return sw_results

def attri_sensitive_hashtag(weibo_list):
    sw_hashtag = {}
    for item in weibo_list:
        text = item['text']
        if not isinstance(text, str):
            text = text.encode('utf-8', 'ignore')
        sw_dict = sensitive_words_extract(text)
        if not sw_dict:
            continue
        text = text.decode('utf-8', 'ignore')
        RE = re.compile(u'#([a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+)#', re.UNICODE)
        hashtag_list = RE.findall(text)
        if not hashtag_list:
            continue
        for hashtag in hashtag_list:
            if sw_hashtag.has_key(hashtag):
                sw_hashtag[hashtag] += 1
            else:
                sw_hashtag[hashtag] = 1

    return sw_hashtag

def temporary_text_update(user, weibo_list): # uid, [weibo_text]
    result = {}
    result['text_len'] = attr_text_len(weibo_list)
    result['emotion'] = json.dumps(attr_emoticon(weibo_list))
    result['emotion_words'] = json.dumps(attr_liwc(weibo_list))
    result['link'] = attr_link(weibo_list)
    #result['online_pattern'] = json.dumps(attr_online_pattern(weibo_list))
    keywords_dict = attr_keywords(weibo_list)
    result['keywords'] = json.dumps(keywords_dict)
    result['keywords_string'] = '&'.join(keywords_dict.keys())

    return result

def compute_text_attribute(user, weibo_list):
    result = {}
    temporary_text_dict = temporary_text_update(user, weibo_list)
    result.update(temporary_text_dict)
    # result['domain'] = attri_domain(weibo_list)
    result['domain'] = 'test_domain'
    result['domain_string'] = "&".join(result['domain'])
    # result['psycho_status'] = attr_psycho_status(user, weibo_list)
    # result['psycho_status_string'] = '&'.join(result['psycho_status'].keys())
    result['psycho_status'] = json.dumps({'level1':{'status1':1, 'status2':2}, 'level2':{'status1':1, 'status2':2}})
    result['psycho_status_string'] = 'status1&status2'
    #result['topic'] = attr_topic(weibo_list)
    #result['topic_string'] = '&'.join(result['topic'].keys())
    result['topic'] = json.dumps({'art':1, 'education':2})
    result['topic_string'] = 'art&education'
    #sensitive_dict = attri_sensitive_words(weibo_list)
    #result['sensitive_words'] = json.dumps(sensitive_dict)
    #result['sensitive_words_string'] = '&'.join(sensitive_dict.keys())
    #sensitive_hashtag = attri_sensitive_hashtag(weibo_list)
    #result['sensitive_hashtag'] = json.dumps(sensitive_hashtag)
    #result['sensitvie_hashtag_string'] = '&'.join(sensitive_hashtag.keys())

    return result

def read_uid_list():
    date = ts2datetime(time.time()-24*3600)
    date = date.replace('-','')
    sensitive_dict = r.hgetall('identify_in_sensitive_'+str(date))
    influence_dict = r.hgetall('identify_in_influence_'+str(date))
    uid_list = []
    for uid in sensitive_dict:
        if sensitive_dict[uid] != '3':
            uid_list.append(uid)
    for uid in influence_dict:
        if influence_dict[uid] != '3':
            uid_list.append(uid)

    return uid_list

def compute_attribute(user_weibo_dict):
    # test
    uid_list = user_weibo_dict.keys()
    times = len(uid_list)/1000
    bulk_action = []
    count = 0
    count_list = set()
    for i in range(times+1):
        flow_result = get_flow_information(uid_list[1000*i:1000*(i+1)]) # 流数据更新
        register_result = get_profile_information(uid_list) # 背景信息数据更新
        for user in uid_list:
            weibo_list = user_weibo_dict[user]
            results = compute_text_attribute(user, weibo_list) # 文本属性计算
            results['uid'] = str(user)
            flow_dict = flow_result[str(user)]
            results.update(flow_dict)
            user_info = {'uid':str(user), 'domain':results['domain'], 'topic':results['topic'], 'activity_geo':results['geo_string']}
            evaluation_index = get_evaluate_index(user_info, status='insert')
            results.update(evaluation_index)
            register_dict = register_result[user]
            results.update(register_dict)
            action = {'index':{'_id':str(user)}}
            bulk_action.extend([action, results])
            count_list.add(user)
            count += 1
            if count % 200 == 0:
                es.bulk(bulk_action, index='sensitive_user_portrait_0103', doc_type="user", timeout=60)
                bulk_action = []
                print count
    if bulk_action:
        es.bulk(bulk_action, index='sensitive_user_portrait_0103', doc_type="user", timeout=60)
    return "1"

'''
def update_portrait():
    user_weibo_dict = read_user_weibo()
    uid_list = user_weibo_dict.keys()
    flow_result = get_flow_information(uid_list)
    bulk_action = []
    count = 0
    for user in uid_list:
        action = {'update':{'_id': str(user)}}
        result = {'doc':flow_result[user]}
        bulk_action.extend([action, result])
        count += 1
        if count % 500 == 0:
            es.bulk(bulk_action, index='sensitive_user_portrait', doc_type='user', timeout=60)
            bulk_action = []
            print count
    if bulk_action:
        es.bulk(bulk_action, index='sensitive_user_portrait', doc_type='user', timeout=60)
    return '1'
'''
if __name__ == '__main__':
    #compute_attribute()
    update_portrait()
