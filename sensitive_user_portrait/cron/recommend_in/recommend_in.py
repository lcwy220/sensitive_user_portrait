# -*- coding=utf-8 -*-

# select high influence user and sensitive weibo user to recommend in

import sys
from elasticsearch import Elasticsearch
from filter_rules import filter_rules, filter_recommend, save_recommentation2redis, read_black_user_list

reload(sys)
sys.path.append('../../')
from global_config import RECOMMENTATION_TOPK as top_k
from global_utils import ES_CLUSTER_FLOW1 as es_cluster
from global_utils import R_RECOMMENTATION as r_recommend

def search_sensitive_weibo(index_name):
    # sensitive weibo user recommend
    query_body={
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "should":[
                            {"range":{"s_retweeted_weibo_number":{"gt":0}}},
                            {"range":{"s_origin_weibo_number":{"gt":0}}}
                        ]
                    }
                }
            }
        },
        "size":10000000
    }

    result = es_cluster.search(index=index_name, doc_type="bci", body=query_body)['hits']['hits']
    sensitive_uid = []
    for item in result:
        sensitive_uid.append(item['_source']['uid'])

    return sensitive_uid

def search_top_k(index_name, top_k):
    # top_k recommend
    query_body={
        "query":{
            "match_all":{}
        },
        "size":top_k,
        "sort": [{"user_index": {"order": "desc"}}]
    }

    result = es_cluster.search(index=index_name,doc_type="bci", body=query_body)["hits"]["hits"]
    sensitive_uid = []
    for item in result:
        sensitive_uid.append(item['_source']['uid'])

    return sensitive_uid



if __name__ == "__main__":
    now_date = ts2datetime(time.time()).replace('-','')
    now_date = '20130901' # test
    sensitive_weibo_uid = search_sensitive_weibo(now_date) # sensitive words uid list, direct recommend in
    top_influence_uid = search_top_k(now_date, top_k) # top influence uid list, filter

    # step 1: no sensitive user in top influence
    revise_influence_uid_list = set(top_influence_uid) - set(sensitive_weibo_uid)
    black_uid_list = read_black_user_list()
    revise_influence_uid_list = set(revise_influence_uid_list) - set(black_uid_list)
    print 'filter black list: ', len(revise_influence_uid_list)
    #total = set(sensitive_weibo_uid) | set(top_influence_uid)
    # step 2: no recommending
    sensitive_uid_recommending_filter = filter_recommend(sensitive_weibo_uid)
    top_influence_recommending_filter = filter_recommend(revise_influence_uid_list)
    # step 3: no one in portrait
    sensitive_uid_in_filter = filter_in(sensitive_uid_recommending_filter)
    top_influence_in_filter = filter_in(top_influence_recommending_filter)

    print len(sensitive_uid_in_filter)
    print len(top_influence_in_filter)

    top_influence_filter_result = filter_rules(top_influence_in_filter)

    if sensitive_uid_in_filter:
        r_recommend.hset('recommend_sensitive', now_date, json.dumps(sensitive_uid_in_filter))
    else:
        r_recommend.hset('recommend_sensitive', now_date, '0')

    if top_influence_filter_result:
        r_recommend.hset('recommend_influence', now_date, json.dumps(top_influence_in_filter))
    else:
        r_recommend.hset('recommend_influence', now_date, '0')


