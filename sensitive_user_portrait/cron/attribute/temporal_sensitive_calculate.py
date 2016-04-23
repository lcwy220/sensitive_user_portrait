# -*- coding:utf-8 -*-

import redis
import time
import json
import math
from elasticsearch import Elasticsearch
from text_attribute import compute_attribute

es_text = Elasticsearch("219.224.135.93:9206", timeout=60)
es_cluster = Elasticsearch("219.224.135.93:9206", timeout=60)

def query_size(size, start):
    rank_query_body = {
        "query": {
            "match_all" :{}
        },
        "sort": {"user_index": {"order": "desc"}},
        "from": start,
        "size": size
    }

    return rank_query_body

if __name__ == "__main__":
    uid_list = []
    search_result = es_cluster.search(index="20130907", doc_type="bci", body=query_size(10000,0))["hits"]["hits"]
    for item in search_result:
        uid_list.append(item['_id'])
    print len(uid_list)
    uid_list.append("1263387643")

    count = 0
    length = len(uid_list)
    partion = 200
    number = int(math.ceil(length*1.0/partion))
    print number
    user_list = [] # 每次迭代计算的用户id_list
    for i in range(number):
        user_list = uid_list[i*partion:(i+1)*partion-1]
        query_body = {
            "query": {
                "filtered": {
                    "filter": {
                        "bool": {
                            "should": [
                            ]
                        }
                    }
                }
            },
            "size": 100000
        }
        for iter_item in user_list:
            query_body["query"]["filtered"]["filter"]["bool"]["should"].append({"term": {"uid": iter_item}})

        text_result = es_text.search(index="sensitive_user_text", doc_type="user", body=query_body)["hits"]['hits']
        bulk_action = []
        count_c = 0
        weibo_user_dict = dict()
        for item in text_result:
            iter_uid = item["_source"]["uid"]
            if weibo_user_dict.has_key(iter_uid):
                weibo_user_dict[iter_uid].append(item["_source"])
            else:
                weibo_user_dict[iter_uid] = [item["_source"]]
            count_c += 1
        print "weibo_user_dict: ", len(weibo_user_dict)
        print "times: ", i
        if weibo_user_dict:
            compute_attribute(weibo_user_dict)


