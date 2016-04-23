# -*- coding:utf-8 -*-

import math
import redis
import json
from elasticsearch import Elasticsearch
from global_utils import R_CLUSTER_FLOW1 as r_cluster
from DFA_filter import sensitive_words_extract

es_flow_text = Elasticsearch("219.224.135.93:9206", timeout=600)
weibo_redis = redis.StrictRedis("219.224.135.97", "6379", 1)

query_body = {
    "query":{
        "filtered":{
            "filter":{
                "bool":{
                    "should":[
                    ]
                }
            }
        }
    },
    "size": 10000
}


if __name__ == "__main__":
    scan_cursor = 0
    sensitive_uid_list = []
    count = 0
    while 1:
        re_scan = r_cluster.sscan('s_user_set', scan_cursor, count=10000)
        if int(re_scan[0]) == 0:
            sensitive_uid_list.extend(re_scan[1])
            count += len(re_scan[1])
            print count
            break
        else:
            sensitive_uid_list.extend(re_scan[1])
            count += 10000
            scan_cursor = re_scan[0]

    temp_list = sensitive_uid_list
    count = 0
    patition = 100
    number = int(math.ceil(len(temp_list)/float(100)))
    print number
    bulk_action = []


    for i in range(number):
        print i
        uid_list = temp_list[i*patition:(i+1)*patition]
        for uid in uid_list:
            query_body["query"]["filtered"]["filter"]["bool"]["should"].append({"term":{"uid": uid}})
        es_result = es_flow_text.search(index="flow_text_2013-09-01",doc_type="text", body=query_body)["hits"]["hits"]
        for item in es_result:
            source = item["_source"]
            text = source["text"].encode("utf-8", "ignore")
            sensitive_dict = sensitive_words_extract(text)
            sensitive = sensitive_dict
            if sensitive:
                source["sensitive"] = 1
                source["sensitive_words"] = json.dumps(sensitive_dict)
            else:
                source["sensitive"] = 0
            _id = source["mid"]
            action = {"index": {"_id": _id}}
            bulk_action.extend([action, source])
            count += 1
            if count % 1000 == 0:
                es_flow_text.bulk(bulk_action, index="sensitive_user_text_111", doc_type="user")
                bulk_action = []
                print count
    if bulk_action:
        es_flow_text.bulk(bulk_action, index="sensitive_user_text_111", doc_type="user")
    print count




