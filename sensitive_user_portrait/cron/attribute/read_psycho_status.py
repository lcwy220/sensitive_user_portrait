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

domain_dict = {"media":"独立媒体人", "official-media":"官方媒体", "root":"草根红人", "non-public":"非公企业主", \
"governer":"公职人员", "well-known": "公知分子", 'writer':"作家写手", "professor":"专家学者", "welfare":"社会公益", \
"lawyer": "维权律师", "star": "文体明星", "religion": "宗教人士"}
'''
csv_file = file('domain1013.csv', 'rb')
reader = csv.reader(csv_file)
for line in reader:
    count += 1
    uid = line[0]
    result = dict()
    results = dict()
    try:
        for i in range(1,13):
            item = line[i].split('*')
            number = item[0].split('E')
            result[item[1]] = int(number[1][1:])
    except:
        print number, count, uid
        continue
    sort_list =  sorted(result.items(), key=lambda x:x[1], reverse=False)
    results['domain'] = domain_dict[sort_list[0][0]]
    action = {"update": {'_id': uid}}
    bulk_action.extend([action, {'doc': results}])
    if count % 100 == 0:
        es.bulk(bulk_action, index='sensitive_user_portrait', doc_type='user', timeout=60)
        bulk_action = []
        print count
if bulk_action:
    es.bulk(bulk_action, index='sensitive_user_portrait', doc_type='user', timeout=60)
'''

'''
es.delete(index= 'custom_attribute', doc_type='attribute', id='AVBa32QMGk0Kt7GIxCQW')
es.delete(index= 'custom_attribute', doc_type='attribute', id='AVBa32rwGk0Kt7GIxCQX')
es.delete(index= 'custom_attribute', doc_type='attribute', id='AVBa4Qx7y3nG3t1ED6gr')
'''

#es.update(index="sensitive_user_portrait", doc_type="user", id=1408848023, body={"doc": {"domain": "公知分子"}})
es.update(index="sensitive_user_portrait", doc_type="user", id=1892680725, body={"doc":{"domain": "公职人员"}})
