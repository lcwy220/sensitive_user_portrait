# -*- coding: UTF-8 -*-

import sys
import json
import time
import operator
reload(sys)
sys.path.append('../')
from global_utils import es_sensitive_user_portrait as es
from global_utils import es_user_profile, es_flow_text
from time_utils import datetime2ts, ts2datetime, ts2date
from parameter import RUN_TYPE
from get_user_info import get_user_profile

def get_top_mid():
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "range":{
                        "sensitive":{
                            "gt":0
                        }
                    }
                }
            }
        },
        "size":100,
        "sort":{"timestamp":{"order":"desc"}}
    }

    if RUN_TYPE:
        index_name = "flow_text_" + ts2datetime(time.time())
    else:
        index_name = "flow_text_2016-05-20"

    search_results = es_flow_text.search(index=index_name, doc_type="text", body=query_body, _source=False, fields=['root_mid'])['hits']['hits']
    mid_list = []
    for item in search_results:
        if item.get("fields", ''):
            mid_list.append(item['fields']['root_mid'][0])
        else:
            mid_list.append('_id')

    return mid_list

def sort_retweet_sensitive_weibo(sensitive_mid_list):
    #sensitive_mid_list = get_top_mid()
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"terms":{"root_mid":sensitive_mid_list}},
                            {"term":{"message_type":3}}
                        ]
                    }
                }
            }
        },
        "aggs":{
            "all_count":{
                "terms":{"field":"root_uid", "size":20}
            }
        }
    }

    if RUN_TYPE:
        index_name = "flow_text_" + ts2datetime(time.time())
    else:
        index_name = "flow_text_2016-05-20"

    uid_list = []
    results = []
    number = []
    search_results = es_flow_text.search(index=index_name, doc_type="text", body=query_body)["aggregations"]["all_count"]["buckets"]
    for item in search_results:
        uid_list.append(item['key'])
        number.append(item['doc_count'])

    if uid_list:
        results = get_user_profile(uid_list, ['nick_name'])

    for i in range(len(uid_list)):
        results[i].append(number[i])

    return results


def sort_comment_sensitive_weibo(sensitive_mid_list):
    #sensitive_mid_list = get_top_mid()
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"terms":{"root_mid":sensitive_mid_list}},
                            {"term":{"message_type":2}}
                        ]
                    }
                }
            }
        },
        "aggs":{
            "all_count":{
                "terms":{"field":"root_uid", "size":20}
            }
        }
    }

    if RUN_TYPE:
        index_name = "flow_text_" + ts2datetime(time.time())
    else:
        index_name = "flow_text_2016-05-20"

    uid_list = []
    results = []
    number = []
    search_results = es_flow_text.search(index=index_name, doc_type="text", body=query_body)["aggregations"]["all_count"]["buckets"]
    for item in search_results:
        uid_list.append(item['key'])
        number.append(item['doc_count'])

    if uid_list:
        results = get_user_profile(uid_list, ['nick_name'])

    for i in range(len(uid_list)):
        results[i].append(number[i])

    return results



def get_weibo_detail(sensitive_mid_list):
    #sensitive_mid_list = get_top_mid()
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "terms":{"root_mid":sensitive_mid_list}
                }
            }
        },
        "aggs":{
            "all_count":{
                "terms":{"field":"root_mid", "size":100},
                "aggs":{
                    "message_type":{
                        "terms":{
                            "field":"message_type"
                        }
                    }
                }
            }
        }
    }

    if RUN_TYPE:
        index_name = "flow_text_" + ts2datetime(time.time())
        now_ts = time.time()
    else:
        index_name = "flow_text_2016-05-20"
        now_ts = datetime2ts('2016-05-20')

    uid_list = []
    weibo_dict = dict() # weibo
    search_results = es_flow_text.search(index=index_name, doc_type="text", body=query_body)["aggregations"]["all_count"]["buckets"]
    for item in search_results:
        temp_dict = dict()
        temp_dict[item['key']] = item['doc_count']
        detail = item['message_type']['buckets']
        detail_dict = dict()
        for iter_item in detail:
            detail_dict[iter_item['key']] = iter_item['doc_count']
        temp_dict['retweeted'] = detail_dict.get("3", 0)
        temp_dict['comment'] = detail_dict.get("2", 0)
        weibo_dict[item['key']] = temp_dict

    weibo_mid_list = weibo_dict.keys()
    results = []
    uid_list = []
    index_list = [index_name]
    for i in range(2):
        now_ts -= 3600*24
        forward_index = "flow_text_" + ts2datetime(now_ts)
        exist_bool = es_flow_text.indices.exists(index=forward_index)
        if exist_bool:
            index_list.append(forward_index)

    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "terms":{"mid":weibo_mid_list}
                }
            }
        },
        "size":10000
    }

    if weibo_mid_list:
        weibo_detail = es_flow_text.search(index=index_list, doc_type='text', body=query_body)["hits"]["hits"]
    else:
        weibo_detail = []
    for item in weibo_detail:
        iter_mid = item['_id']
        item_detail = item['_source']
        uid_list.append(item_detail['uid'])
        temp = []
        temp.extend([item_detail['text'], ts2date(item_detail['timestamp']),item_detail['geo'].replace('&', " ")])
        if item_detail.get("sensitive_words_string", ''):
            temp.append(item_detail["sensitive_words_string"].split('&'))
        else:
            temp.append([])
        temp.append(item_detail.get('sensitive',0))
        temp.append(weibo_dict[iter_mid]['retweeted'])
        temp.append(weibo_dict[iter_mid]['comment'])
        results.append(temp)

    if uid_list:
        user_profile_list = get_user_profile(uid_list, ['nick_name'])
    else:
        user_profile_list = []
    if user_profile_list:
        for i in range(len(user_profile_list)):
            results[i].extend(user_profile_list[i])

    results = sorted(results, key=operator.itemgetter(-5, -4), reverse=True)
    return results




if __name__ == "__main__":
    mid_list = get_top_mid()
    print sort_retweet_sensitive_weibo(mid_list)
    #print get_weibo_detail(mid_list)



