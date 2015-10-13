# -*- coding:utf-8 -*-
import csv
import json
import sys
from elasticsearch import Elasticsearch
reload(sys)
sys.path.append('./../../')
from global_utils import es_sensitive_user_portrait as es

count = 0
bulk_action = []

'''
with open ('result_1010.csv', 'rb') as f:
    for line in f:
        count += 1
        results = {}
        line = line.strip().split(',')
        results['uid'] = line[0]
        results['positive'] = line[1].split('*')[0]
        results['negetive'] = line[2].split('*')[0]
        results['middle'] = line[3].split('*')[0]
        results['anger'] = line[4].split('*')[0]
        results['other'] = line[5].split('*')[0]
        results['anxious'] = line[6].split('*')[0]
        results['sad'] = line[7].split('*')[0]
        temp = dict()
        temp['psycho_status'] = json.dumps(results)
        action = {"update": {'_id': results['uid']}}
        bulk_action.extend([action, {'doc': temp}])
        if count % 500 == 0:
            es.bulk(bulk_action, index='sensitive_user_portrait', doc_type='user', timeout=60)
            bulk_action = []
            print count
    if bulk_action:
        es.bulk(bulk_action, index='sensitive_user_portrait', doc_type='user', timeout=60)

with open ('1010_domain.csv', 'rb') as f:
    for line in f:
        count += 1
        results = {}
        line = line.strip().split(',')
        uid = line[0].strip()
        results['politics_trend'] = line[1].strip()
        action = {"update": {'_id': uid}}
        bulk_action.extend([action, {'doc': results}])
        if count % 100 == 0:
            es.bulk(bulk_action, index='sensitive_user_portrait', doc_type='user', timeout=60)
            bulk_action = []
            print count
    if bulk_action:
        es.bulk(bulk_action, index='sensitive_user_portrait', doc_type='user', timeout=60)

'''

print json.loads(es.get(index='20130907', doc_type="bci", id='2988136341')['_source']['retweeted_weibo_comment_detail'])

