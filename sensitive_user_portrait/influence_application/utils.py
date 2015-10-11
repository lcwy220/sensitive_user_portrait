# -*- coding:utf-8 -*-

import time
import sys
from elasticsearch import Elasticsearch
from user_list import domain_dict
from sensitive_user_portrait.global_utils import ES_CLUSTER_FLOW1 as es_cluster
from sensitive_user_portrait.global_utils import es_sensitive_user_portrait as es
from sensitive_user_portrait.global_utils import es_user_profile
from sensitive_user_portrait.time_utils import ts2datetime, datetime2ts



def search_domain(domain, date, number=100):
    # top influence user in domain
    count = 0
    count_n = 0
    result_list = []
    date = str(date).replace('-', '')

    query_body = {
        "query":{
            "match_all": {}
        },
        "sort": {date: {"order": "desc"}},
        "size": 1+count
    }

    while 1:
        search_results = es.search(index='copy_sensitive_user_portrait', doc_type='user', body=query_body)['hits']['hits']
        uid_list = []
        count += 1
        for item in search_results:
            uid_list.append(item['_id'])
        portrait_results = es.mget(index='sensitive_user_portrait', doc_type='user', body={"ids":uid_list})['docs']
        for item in portrait_results:
            domain_list = (item['_source']['topic_string']).split('&')
            if domain in set(domain_list):
                result_list.append([item['_id'], item['_source']['uname'], item['_source']['photo_url'], item['_source']['influence'], item['_source']['sensitive'], item['_source']['importance'], item['_source']['activeness']])
                count_n += 1
        if count_n >= int(number):
            break

    return result_list

def search_current_es(domain, date, number):
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"term": {"topic_string": domain}}
                        ]
                    }
                }
            }
        },
        'sort': {"influence": {"order": "desc"}},
        'size': number
    }

    search_result = es.search(index=date, doc_type='user', body=query_body)['hits']['hits']
    result_list = []
    for item in search_result:
        if not item['_source']['uname']:
            item['_source']['uname'] = 'unknown'
            item['_source']['photo_url'] = 'unknown'
        result_list.append([item['_id'], item['_source']['uname'], item['_source']['photo_url'], item['_source']['influence'], item['_source']['sensitive'], item['_source']['importance'], item['_source']['activeness']])

    return result_list


def influence_distribute():

    row = [0, 200, 500, 700, 900, 1100, 10000]
    result = []
    ts = time.time()
    ts = datetime2ts('2013-09-08')
    ts = ts - 8*3600*24
    for j in range(7):
        detail = []
        ts += 3600*24
        date = ts2datetime(ts).replace('-', '')
        for i in range(6):
            low_limit = row[i]
            upper_limit = row[i+1]
            query_body = {
                "query": {
                    "filtered": {
                        "filter": {
                            "range": {
                                date: {
                                    "gte": low_limit,
                                    "lt": upper_limit
                                }
                            }
                        }
                    }
                }
            }
            number = es.count(index='copy_sensitive_user_portrait', doc_type="user", body=query_body)['count']
            detail.append(number)
        result.append(detail)
    return result

def test_influence_rank(domain, date):
    uid_list = domain_dict[domain]
    search_result = es.mget(index='copy_sensitive_user_portrait', doc_type="user", body={"ids": uid_list})['docs']
    portrait_result = es.mget(index=)
    for item in search_result:
        



if __name__ == '__main__':
    #print search_domain('art', '20130907', number=10)
    #print search_current_es('art', 'sensitive_user_portrait', number=10)
    print influence_distribute()

