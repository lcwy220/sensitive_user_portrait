# -*-coding:utf-8 -*-

import sys
import re
import IP
import csv
import json
import time
from elasticsearch import Elasticsearch
from DFA_filter import sensitive_words_extract

reload(sys)
sys.path.append('./../../')
from global_utils import R_RECOMMENTATION as r
from global_utils import es_sensitive_user_portrait as es
from time_utils import datetime2ts, ts2datetime

reload(sys)
sys.path.append('../../../../../libsvm-3.17/python/')
from sta_ad import load_scws

sw = load_scws()
cx_dict = ['a', 'n', 'nr', 'ns', 'nz', 'v', '@', 'd']

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

def attr_liwc(text_list):
    results = {}
    keyword_results = {}
    for text in text_list:
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

def ip2geo(ip):
    try:
        city = IP.find(str(ip))
        if city:
            city.encode('utf-8')
        else:
            city=''
    except Exception, e:
        city = ''
    if city:
        len_city = len(city.split('\t'))
        if len_city == 4:
            city = '\t'.join(city.split('\t')[0:3])
    return city

def sensitive_user_text_mapping():
    index_info = {
        "mappings":{
            "user":{
                "properties":{
                    "text":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "mid":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    'ip':{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "timestamp":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "sentiment":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "sensitive_words":{
                        "type": "string",
                        "index": "not_analyzed"
                    },
                    "message_type":{
                        "type":"string",
                        "index": "not_analyzed"
                    },
                    "sensitive":{
                        "type":"string",
                        "index": "not_analyzed"
                    }
                }
            }
        }
    }

    es.indices.create(index="sensitive_user_text", body=index_info, ignore=400)


def save_text2es():
    count = 0
    bulk_action = []
    user_weibo_dict = dict()
    csvfile = open('./sensitive_uid_text_2.csv', 'rb')
    reader = csv.reader(csvfile)
    for line in reader:
        count += 1
        weibo = dict()
        user = line[0]
        weibo['text'] = line[1].decode('utf-8', 'ignore')
        weibo['mid'] = line[2]
        weibo['geo'] = ip2geo(line[3])
        weibo['timestamp'] = line[4]
        weibo['message_type'] = line[5]
        weibo['uid'] = user
        sentiment = attr_liwc([weibo['text']])
        weibo['sentiment'] = json.dumps(sentiment)
        if not isinstance(weibo['text'], str):
            text = (weibo['text']).encode('utf-8', 'ignore')
        sw_dict = sensitive_words_extract(text)
        if sw_dict:
            weibo['sensitive_words'] = json.dumps(sw_dict)
            weibo['sensitive'] = 1
        else:
            weibo['sensitive'] = 0
        action = {'index':{'_id':weibo['mid']}}
        bulk_action.extend([action, weibo])
        if count % 1000 == 0:
            es.bulk(bulk_action, index='sensitive_user_text', doc_type='user', timeout=30)
            bulk_action = []
            print count
    if bulk_action:
        es.bulk(bulk_action, index='sensitive_user_text', doc_type='user', timeout=30)


if __name__ == "__main__":
    sensitive_user_text_mapping()
    save_text2es()
