# -*- coding: UTF-8 -*-

import sys
import json
import time
from sensitive_user_portrait.global_utils import R_RECOMMENTATION as r
from sensitive_user_portrait.global_utils import es_sensitive_user_portrait as es
from sensitive_user_portrait.time_utils import datetime2ts, ts2datetime
from appendix import get_top_user, get_topic_user

def query_body_module(term):
    query_body={
        "aggs":{
            "all_interests":{
                "terms":{"field": term}
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
    results = es.search(index="sensitive_user_portrait", doc_type="user", body=query_body)['hits']['hits']
    uid_list = []
    for item in results:
        uid_list.append(item['_source']['uid'])
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
        uid_list.append(item['_source']['uid'])
    return uid_list


def get_attr(date):
    results = dict()
    number = es.count(index="sensitive_user_portrait", doc_type="user")['count']
    results['total_number'] = number

    query_body={
        "query":{
            "filtered":{
                "filter":{
                    "term":{
                        "type": 1
                    }
                }
            }
        }
    }
    sensitive_number = es.count(index="sensitive_user_portrait", doc_type="user", body=query_body)['count']
    results['sensitive_number'] = sensitive_number
    results['influence_number'] = number - sensitive_number

    recommend_in_sensitive = 0
    sensitive_dict = r.hgetall('recommend_sensitive')
    for k,v in sensitive_dict.items():
        if v:
            sensitive_list = json.loads(v)
            recommend_in_sensitive += len(sensitive_list)

    recommend_in_influence = 0
    influence_dict = r.hgetall('recommend_influence')
    for k,v in influence_dict.items():
        if v:
            sensitive_list = json.loads(v)
            recommend_in_influence += len(sensitive_list)
    results['recommend_in'] = recommend_in_influence + recommend_in_sensitive

    results['monitor_number'] = [4, 83] # test
    results['new_sensitive_words'] = 5  # test

    query_body = query_body_module('sensitive_words_string')
    sw_list =  es.search(index='sensitive_user_portrait', doc_type='user', body=query_body)['aggregations']['all_interests']['buckets']
    sensitive_words = []
    for item in sw_list:
        temp = []
        temp.append(item['key'])
        temp.append(item['doc_count'])
        sensitive_words.append(temp)
    results['sensitive_words'] = sensitive_words

    query_body = query_body_module('sensitive_hashtag_string')
    sh_list =  es.search(index='sensitive_user_portrait', doc_type='user', body=query_body)['aggregations']['all_interests']['buckets']
    sensitive_hashtag = []
    for item in sh_list:
        temp = []
        temp.append(item['key'])
        temp.append(item['doc_count'])
        sensitive_hashtag.append(temp)
    results['sensitive_hashtag'] = sensitive_hashtag

    query_body = query_body_module('sensitive_geo_string')
    sg_list =  es.search(index='sensitive_user_portrait', doc_type='user', body=query_body)['aggregations']['all_interests']['buckets']
    sensitive_geo = []
    for item in sg_list:
        temp = []
        temp.append(item['key'])
        temp.append(item['doc_count'])
        sensitive_geo.append(temp)
    results['sensitive_geo'] = sensitive_geo

    query_body = query_body_module('psycho_status_string')
    sp_list = es.search(index='sensitive_user_portrait', doc_type='user', body=query_body)['aggregations']['all_interests']['buckets']
    psycho_status = []
    for item in sp_list:
        temp = []
        temp.append(item['key'])
        temp.append(item['doc_count'])
        psycho_status.append(temp)
    results['psycho_status'] = psycho_status

    '''
    query_body = query_body_module('political_tendency')
    st_list =  es.search(index='sensitive_user_portrait', doc_type='user', body=query_body)['aggregations']['all_interests']['buckets']
    political_tendency = []
    for item in st_list:
        temp = []
        temp.append(item['key'])
        temp.append(item['doc_count'])
        political_tendency.append(temp)
    results['political_tendency'] = political_tendency
    '''
    results['political_tendency'] = [['left', 123], ['middle', 768], ['right', 1095]]

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
    domain_list = ['']
    #search_important('domain', )
    domain_results = get_top_user()
    topic_results = get_topic_user()
    results['domain_rank'] = domain_results
    results['topic_rank'] = topic_results



    # rank
    important_list = search_in_portrait('importance')
    results['importance'] = important_list
    results['sensitive'] = search_in_portrait('sensitive')
    results['influence'] = search_in_portrait('influence')
    results['activeness'] = search_in_portrait('activeness')

    query_body={
        "query":{
            "match_all": {}
        },
        "sort": {"s_origin_weibo_comment_top_number": {"order": "desc"}}
    }
    date = ts2datetime(time.time()-24*3600).replace('-','')
    date = '20130907'
    results_list = es.search(index=date, doc_type="bci", body=query_body)['hits']['hits']
    comment_weibo_detail = []
    for item in results_list:
        temp = []
        temp.append(item['_source']['uid'])
        temp.append(item['_source']['s_origin_weibo_top_comment_id'])
        temp.append(item['_source']['s_origin_weibo_comment_top_number'])
        comment_weibo_detail.append(temp)
    results['top_comment'] = comment_weibo_detail

    query_body={
        "query":{
            "match_all": {}
        },
        "sort": {"s_origin_weibo_retweeted_top_number": {"order": "desc"}}
    }
    date = ts2datetime(time.time()-24*3600).replace('-','')
    date = '20130907'
    results_list = es.search(index=date, doc_type="bci", body=query_body)['hits']['hits']
    retweeted_weibo_detail = []
    for item in results_list:
        temp = []
        temp.append(item['_source']['uid'])
        temp.append(item['_source']['s_origin_weibo_top_retweeted_id'])
        temp.append(item['_source']['s_origin_weibo_retweeted_top_number'])
        comment_weibo_detail.append(temp)
    results['top_retweeted'] = retweeted_weibo_detail



    return results
