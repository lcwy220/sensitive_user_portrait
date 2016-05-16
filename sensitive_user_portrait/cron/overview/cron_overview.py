# -*- coding: UTF-8 -*-

import sys
import json
import time
from get_top_user import get_top_user
from search import get_top_mid, sort_retweet_sensitive_weibo, \
                   sort_comment_sensitive_weibo, get_weibo_detail
reload(sys)
sys.path.append('../../')
from global_utils import R_RECOMMENTATION as r
from global_utils import es_sensitive_user_portrait as es
from global_utils import es_user_profile, es_flow_text, group_index_name, group_index_type
from time_utils import datetime2ts, ts2datetime
from parameter import RUN_TYPE

def query_body_module(term):
    query_body={
        "aggs":{
            "all_interests":{
                "terms":{"field": term, "size":20}
            }
        }
    }
    return query_body

def search_important(category, detail):
    query_body={
        "query":{
            "filtered":{
                "filter":{
                    "term": {category: detail}
                 }
            }
        },
        "sort": {"sensitive": {"order": "desc"}},
        "size": 20
    }
    results = es.search(index="sensitive_user_portrait", doc_type="user", body=query_body, _source=False, fields=['uname'])['hits']['hits']
    uid_list = []
    for item in results:
        uid_list.append([item['_id'], item['fields']['uname'][0]])
    return uid_list


def search_in_portrait(category):
    query_body={
        "query":{
            "match_all": {}
        },
        "sort": {category: {"order": "desc"}}
    }
    results = es.search(index="sensitive_user_portrait", doc_type="user", body=query_body)['hits']['hits']
    uid_list = []
    for item in results:
        uid_list.append([item['_source']['uid'], item['_source']['uname'], item['_source'][category]])
    return uid_list


def get_attr(date):
    results = dict()
    total_number = es.count(index="sensitive_user_portrait", doc_type="user")['count']
    results['total_number'] = total_number

    query_body={
        "query":{
            "filtered":{
                "filter":{
                    "term":{
                        "sensitive": 0
                    }
                }
            }
        }
    }
    influence_number = es.count(index="sensitive_user_portrait", doc_type="user", body=query_body)['count']
    results['sensitive_number'] = total_number - influence_number
    results['influence_number'] = influence_number

    # 政治倾向性统计
    query_body = query_body_module('politics')
    politic_array =  es.search(index='sensitive_user_portrait', doc_type='user', body=query_body)['aggregations']['all_interests']['buckets']
    politic_dict = dict()
    for item in politic_array:
        politic_dict[item['key']] = item['doc_count']
    results['politics'] = politic_dict

    # 入库推荐人数
    recommend_in_sensitive = 0
    recommend_in_sensitive = r.hlen("recomment_" + date +'sensitive')

    recommend_in_influence = 0
    recommend_in_influence = r.hlen("recomment_" + date + "_influence")
    results['recommend_in'] = recommend_in_influence + recommend_in_sensitive

    # 群体分析任务
    results['monitor_number'] = [4, 83] # test
    query_body = {
        "query":{
            "bool":{
                "must":[
                    {"term":{'task_type':"detect"}},
                    {"term":{"state":0}}
                ]
            }
        }
    }
    group_detect_number = es.count(index=group_index_name, doc_type=group_index_type, body=query_body)["count"]
    query_body = {
        "query":{
            "bool":{
                "must":[
                    {"term":{'task_type':"analysis"}},
                    {"term":{"state":0}}
                ]
            }
        }
    }
    group_analysis_number = es.count(index=group_index_name, doc_type=group_index_type, body=query_body)["count"]
    results["group_detect_number"] = group_detect_number
    results["group_analysis_number"] = group_analysis_number


    # 敏感词
    query_body = query_body_module('sensitive_words_string')
    sw_list =  es.search(index='sensitive_user_portrait', doc_type='user', body=query_body)['aggregations']['all_interests']['buckets']
    sensitive_words = []
    for item in sw_list:
        temp = []
        temp.append(item['key'])
        temp.append(item['doc_count'])
        sensitive_words.append(temp)
    results['sensitive_words'] = sensitive_words

    query_body = query_body_module('keywords_string')
    sg_list =  es.search(index='sensitive_user_portrait', doc_type='user', body=query_body)['aggregations']['all_interests']['buckets']
    sensitive_geo = []
    for item in sg_list:
        temp = []
        temp.append(item['key'])
        temp.append(item['doc_count'])
        sensitive_geo.append(temp)
    results['keywords_string'] = sensitive_geo

    query_body = query_body_module('sensitive_hashtag_string')
    sh_list =  es.search(index='sensitive_user_portrait', doc_type='user', body=query_body)['aggregations']['all_interests']['buckets']
    sensitive_hashtag = []
    for item in sh_list:
        temp = []
        temp.append(item['key'])
        temp.append(item['doc_count'])
        sensitive_hashtag.append(temp)
    results['sensitive_hashtag'] = sensitive_hashtag

    query_body = query_body_module('sensitive_activity_geo_aggs')
    sg_list =  es.search(index='sensitive_user_portrait', doc_type='user', body=query_body)['aggregations']['all_interests']['buckets']
    sensitive_geo = []
    for item in sg_list:
        temp = []
        temp.append(item['key'])
        temp.append(item['doc_count'])
        sensitive_geo.append(temp)
    results['sensitive_geo'] = sensitive_geo


    '''
    query_body = query_body_module('domain_string')
    sd_list =  es.search(index='sensitive_user_portrait', doc_type='user', body=query_body)['aggregations']['all_interests']['buckets']
    domain = []
    for item in sd_list:
        temp = []
        temp.append(item['key'])
        temp.append(item['doc_count'])
        domain.append(temp)
    results['domain'] = domain
    '''

    # tendency distribution


    # domain and topic
    rank_results = get_top_user()
    results.update(rank_results)



    # rank
    results['importance'] = search_in_portrait('importance')
    results['sensitive'] = search_in_portrait('sensitive')
    results['influence'] = search_in_portrait('influence')
    results['activeness'] = search_in_portrait('activeness')

    # 敏感微博转发量和评论量
    mid_list = get_top_mid()
    sensitive_hot_retweet = sort_retweet_sensitive_weibo(mid_list)
    sensitive_hot_comment = sort_comment_sensitive_weibo(mid_list)
    sensitive_weibo_text = get_weibo_detail(mid_list)

    results['sensitive_hot_retweet'] = sensitive_hot_retweet
    results['sensitive_hot_comment'] = sensitive_hot_comment
    results['sensitive_weibo_text'] = sensitive_weibo_text

    r.set('overview', json.dumps(results))


if __name__ == "__main__":
    if RUN_TYPE:
        date = ts2datetime(time.time())
        get_attr(date)
    else:
        get_attr('2013-09-02')


