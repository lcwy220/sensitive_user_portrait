# -*- coding: UTF-8 -*-

import IP
import sys
import math
import time
import json
import redis
from sensitive_user_portrait.get_user_info import get_user_profile, get_user_portrait, normalize_index
from sensitive_user_portrait.global_utils import es_user_portrait, portrait_index_name,portrait_index_type
from sensitive_user_portrait.global_utils import es_user_profile, profile_index_name, profile_index_type
from sensitive_user_portrait.global_utils import es_flow_text,ES_CLUSTER_FLOW1,es_sensitive_history
from sensitive_user_portrait.time_utils import ts2datetime, datetime2ts, ts2date
from sensitive_user_portrait.parameter import RUN_TYPE

def get_history_max():
    max_results = {}
    bci_max = ES_CLUSTER_FLOW1.search(index="bci_history", doc_type="bci", body={"query":{"match_all":{}}, "size":1, \
            "sort":{"bci_day_last":{"order":"desc"}}})["hits"]["hits"]
    sensitive_max = es_sensitive_history.search(index="sensitive_history", doc_type="sensitive", body={"query":{"match_all":{}},\
            "size":1,"sort":{"last_value":{"order":"desc"}}})["hits"]["hits"]
    max_results["max_bci"] = bci_max[0]["_source"]["bci_day_last"]
    max_results["max_sensitive"] = sensitive_max[0]["_source"]["last_value"]

    return max_results

def get_evaluate_max():
    max_result = {}
    evaluate_index = ['activeness', 'importance', 'influence', 'sensitive']
    for evaluate in evaluate_index:
        query_body = {
            'query':{
                'match_all':{}
            },
            'size':1,
            'sort':[{evaluate: {'order': 'desc'}}]
        }
        result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)['hits']['hits']
        max_evaluate = result[0]['_source'][evaluate]
        if max_evaluate != 0:
            max_result[evaluate] = max_evaluate
        else:
            max_result[evaluate] = 99999

    return max_result

def search_portrait(condition_num, query, sort, size):
    user_result = []
    index_name = portrait_index_name
    index_type = portrait_index_type
    search_result_max = get_evaluate_max()
    if condition_num > 0:
        result = es_user_portrait.search(index=index_name, doc_type=index_type, \
        body={'query':{'bool':{'must':query}}, 'sort':[{sort:{'order':'desc'}}], 'size':size})['hits']['hits']
    else:
        result = es_user_portrait.search(index=index_name, doc_type=index_type, \
        body={'query':{'match_all':{}}, 'sort':[{sort:{"order":"desc"}}], 'size':size})['hits']['hits']

    if result:
        for item in result:
            user_dict = item['_source']
            score = item['_score']
            result_normal_activeness = math.log(user_dict['activeness'] / float(search_result_max['activeness']) * 9 + 1, 10)
            result_normal_importance = math.log(user_dict['importance'] / float(search_result_max['importance']) * 9 + 1, 10)
            result_normal_influence = math.log(user_dict['influence'] / float(search_result_max['influence']) * 9 + 1, 10)
            result_normal_sensitive = math.log(user_dict['sensitive'] / float(search_result_max['sensitive']) * 9 + 1, 10)
            user_dict['activeness'] = result_normal_activeness*100
            user_dict['importance'] = result_normal_importance*100
            user_dict['influence'] = result_normal_influence*100
            user_dict['sensitive'] = result_normal_sensitive*100
            user_result.append([user_dict['uid'], user_dict['uname'], user_dict['location'], user_dict['activeness'],\
                user_dict['importance'], user_dict['influence'], user_dict['sensitive'], score])

    return user_result


def full_text_search(keywords, uid, start_time, end_time, size):
    results = []
    uid_list = []
    user_profile_list = []
    query_body = {
        "query": {
                    "bool": {
                        "must": []
                    }
        },
        "size":size,
        "sort":{"timestamp":{"order": 'desc'}}
    }

    if RUN_TYPE:
        query_body["sort"] = {"user_fansnum":{"order": 'desc'}}

    if uid:
        query_body["query"]["bool"]["must"].append({"term":{"uid":uid}})

    if keywords:
        keywords_list = keywords.split(',')
        for word in keywords_list:
            query_body["query"]["bool"]["must"].append({'wildcard':{'text':{'wildcard':'*'+word+'*'}}})

    index_list = []
    exist_bool = es_flow_text.indices.exists(index="flow_text_"+end_time)
    if start_time:
        start_ts = datetime2ts(start_time)
        end_ts = datetime2ts(end_time)
        ts = end_ts
        while 1:
            index_name = "flow_text_"+ts2datetime(ts)
            exist_bool = es_flow_text.indices.exists(index=index_name)
            if exist_bool:
                index_list.append(index_name)
            if ts == start_ts:
                break
            else:
                ts -= 3600*24

    print index_list
    #  没有可行的es
    if not index_list:
        return [[], []]

    search_results = es_flow_text.search(index=index_list, doc_type="text", body=query_body)["hits"]["hits"]
    for item in search_results:
        uid_list.append(item['_source']['uid'])
    user_info = []
    if uid_list:
        history_max = get_history_max()
        personal_field = ["nick_name", "fansnum", "statusnum","user_location"]
        user_info = get_user_profile(uid_list, personal_field)
        bci_results = ES_CLUSTER_FLOW1.mget(index="bci_history", doc_type="bci", body={"ids":uid_list}, _source=False, fields=["bci_day_last"])["docs"]
        in_portrait = es_user_portrait.mget(index="sensitive_user_portrait", doc_type="user", body={"ids":uid_list}, _source=False)["docs"]
        sensitive_results = es_sensitive_history.mget(index="sensitive_history", doc_type="sensitive", body={"ids":uid_list}, _source=False, fields=["last_value"])["docs"]
    print "len search: ", len(search_results)

    count = 0
    # uid uname text date geo sensitive_words retweeted comment
    for item in search_results:
        item = item['_source']
        uid_list.append(item['uid'])
        iter_item = []
        iter_item.append(item['uid'])
        iter_item.append(user_info[count][1])
        iter_item.append(item['text'])
        iter_item.append(ts2date(item['timestamp']))
        iter_item.append(item['geo'])
        if item.get("sensitive_words_string", ''):
            iter_item.append(item['sensitive_words_string'].split('&'))
        else:
            iter_item.append([])
        iter_item.append(item.get('retweeted', 0))
        iter_item.append(item.get('comment', 0))
        count += 1
        results.append(iter_item)

    user_set = set()
    count = 0
    # uid "nick_name", "fansnum", "statusnum","user_location", bci, sensitive
    for item in user_info:
        if item[0] in user_set:
            continue
        else:
            user_set.add(item[0])
        if bci_results[count]["found"]:
            bci_value = bci_results[count]["fields"]["bci_day_last"][0]
            item.append(normalize_index(bci_value, history_max["max_bci"]))
        else:
            item.append(0)
        if sensitive_results[count]["found"]:
            sensitive_value = sensitive_results[count]['fields']['last_value'][0]
            item.append(normalize_index(sensitive_value, history_max["max_sensitive"]))
        else:
            item.append(0)
        if in_portrait[count]["found"]:
            item.append("1")
        else:
            item.append("0")
        user_profile_list.append(item)

    return results, user_profile_list

