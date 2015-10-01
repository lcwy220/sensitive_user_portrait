# -*- coding: UTF-8 -*-
import csv
import sys
from elasticsearch import Elasticsearch
from text_attribute import attr_liwc
reload(sys)
sys.path.append('./../../')
from global_utils import es_sensitive_user_portrait as es
from global_utils import es_user_profile


'''
# read from weibo api
def read_user_weibo(uid_list):
    user_weibo_dict = dict()
    return user_weibo_dict
'''
def sensitive_text_mapping():
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
                    "message_type": {
                        "type": "string",
                        "index": "not_analyzed"
                    },
                }
            }
        }
    }

    es.indices.create(index="sensitive_text", body=index_info, ignore=400)
# test: read user weibo
def read_user_weibo(uid_list=[]):
    count = 0
    bulk_action = []
    user_weibo_dict = dict()
    csvfile = open('./sensitive_uid_text.csv', 'rb')
    reader = csv.reader(csvfile)
    for line in reader:
        count += 1
        weibo = dict()
        user = line[0]
        weibo['uname'] = 'unknown'
        weibo['text'] = line[1].decode('utf-8')
        try:
            user_weibo_dict[user].append(weibo)
        except:
            user_weibo_dict[user] = [weibo]

    return user_weibo_dict

def save_text2es(uid_list=[]):
    count = 0
    bulk_action = []
    user_weibo_dict = dict()
    csvfile = open('./sensitive_uid_text.csv', 'rb')
    reader = csv.reader(csvfile)
    for line in reader:
        count += 1
        weibo = dict()
        user = line[0]
        weibo['uname'] = 'unknown'
        weibo['text'] = line[1].decode('utf-8')
        weibo['online_pattern'] = 'weibo.com'
        weibo['mid'] = line[2]
        weibo['ip'] = line[3]
        weibo['timestamp'] = line[4]
        weibo['uid'] = user
        sentiment = attr_liwc([weibo['text']])
        print sentiment
        sys.exit(0)
        action = {'index':{'_id':weibo['mid']}}
        bulk_action.extend([action, weibo])
        if count % 500 == 0:
            es.bulk(bulk_action, index='monitor_sensitive_text', doc_type='user', timeout=30)
            bulk_action = []
    if bulk_action:
        es.bulk(bulk_action, index='monitor_sensitive_text', doc_type='user', timeout=30)

    return user_weibo_dict
if __name__ == '__main__':
    sensitive_text_mapping()
    read_user_weibo()
