 #-*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from sensitive_user_portrait.global_utils import es_user_profile, es_sensitive_user_portrait, es_flow_text, es_tag
from sensitive_user_portrait.global_utils import portrait_index_name, portrait_index_type, flow_text_index_name_pre, \
                                                 flow_text_index_type, profile_index_name, profile_index_type, R_ADMIN
from sensitive_user_portrait.time_utils import ts2datetime, datetime2ts
from sensitive_user_portrait.parameter import RUN_TYPE
from utils import search_portrait,full_text_search

mod = Blueprint('search', __name__, url_prefix='/search')

@mod.route('/portrait_search/')
def ajax_portrait_search():
    stype = request.args.get('stype', 2)
    stype = int(stype)
    result = {}
    query_data = {}
    query = []
    query_list = []
    condition_num = 0

    if stype == 1:
        fuzz_item = ['uid', 'uname']
        item_data = request.args.get('term', '')
        for item in fuzz_item:
            if item_data:
                query_list.append({'wildcard':{item:'*'+item_data+'*'}})
                condition_num += 1
        query.append({'bool':{'should':query_list}})
    else:
        simple_item = ['uid', 'uname']
        fuzz_item = ['politics', 'hashtag']
        multi_item = ['domain','topic_string', 'keywords_string','sensitive_words_string','activity_geo' ]
        for item in simple_item:
            item_data = request.args.get(item, '')
            if item_data:
                query.append({'wildcard':{item:'*'+item_data+'*'}})
                condition_num += 1
        for item in fuzz_item:
            item_data = request.args.get(item, '')
            if item_data:
                query.append({'term':{item:item_data}})
                condition_num += 1
        for item in multi_item:
            item_data = request.args.get(item, '')
            if item_data:
                if item == 'activity_geo':
                    item_list = item_data.split('/')
                else:
                    item_list = item_data.split(',')
                query.append({"terms":{item:item_list}})
                condition_num += 1
        # custom_attribute
        tag_item = request.args.get('tag', '')
        if tag_item:
            tag_item_list = tag_item.split(':')
            tag_name = tag_item_list[0]
            tag_value = tag_item_list[1]
            if tag_name and tag_value:
                query.append({"term":{"tag-"+tag_name:tag_value}})
                condition_num += 1

    print condition_num
    print query
    size = 1000
    sort = '_score'
    result = search_portrait(condition_num, query, sort, size)
    return json.dumps(result)


@mod.route('/get_hot_keywords/')
def ajax_get_hot_keywords():
    query_body = {
        "query":{
            "match_all":{}
        },
        "aggs":{
            "hot_words":{
                "terms":{"field": "sensitive_words_string", "size":20}
            }
        }
    }

    sensitive_words = []
    search_results = es_sensitive_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)['aggregations']["hot_words"]['buckets']
    if search_results:
        for item in search_results:
            sensitive_words.append([item['key'],item["doc_count"]])

    return json.dumps(sensitive_words)

@mod.route('/full_text_search/')
def ajax_full_text_search():
    if RUN_TYPE:
        ts = time.time()
    else:
        ts = datetime2ts("2013-09-02")
    now_date = ts2datetime(ts)
    start_time = request.args.get("start_time", now_date) # 2013-09-01
    end_time = request.args.get("end_time", now_date)
    uid = request.args.get("uid", "")
    size = request.args.get("number", 100)
    keywords = request.args.get("keywords", "") # 逗号分隔

    results = full_text_search(keywords, uid, start_time, end_time, size)

    return json.dumps(results)

@mod.route('/profile_search/')
def ajax_profile_search():
    stype = request.args.get('stype', '')
    query = []
    query_list = []
    condition_num = 0
    rank_order = request.args.get('order', '1')
    if rank_order == "0":
        order = [{'statusnum':{'order':'desc'}}]
    elif rank_order == "1":
        order = [{'fansnum':{'order':'desc'}}]
    elif rank_order == "2":
        order = [{'friendsnum':{'order':'desc'}}]
    size = request.args.get('size', 100)

    if stype:
        fuzz_item = ['uid', 'uname']
        item_data = request.args.get('term', '')
        for item in fuzz_item:
            if item_data:
                query_list.append({'wildcard':{item:'*'+item_data+'*'}})
                condition_num += 1
        query.append({'bool':{'should':query_list}})
    else:
        fuzz_item = ['uid', 'nick_name', 'real_name', 'user_location', 'user_email', 'user_birth']
        range_item = ['statusnum','fansnum', 'friendsnum']
        range_item_from = ['statusnum_from', 'fansnum_from', 'friendsnum_from']
        range_item_to = ['statusnum_to', 'fansnum_to', 'friendsnum_to']
        select_item = ['sex', 'tn', 'sp_type']
        for item in fuzz_item:
            item_data = request.args.get(item, '')
            if item_data:
                query.append({'wildcard':{item:'*'+item_data+'*'}})
                condition_num += 1
        for i in range(3):
            from_item = request.args.get(range_item_from[i], 0)
            to_item = request.args.get(range_item_to[i], 1000000000)
            query.append({"range":{range_item[i]:{"from":from_item,"to":to_item}}})
            condition_num += 1
        for item in select_item:
            item_data = request.args.get(item, '')
            if item_data:
                query.append({'match':{item:item_data}})
                condition_num += 1

    if condition_num:
        source = es_user_profile.search(\
                index = "weibo_user", doc_type="user", \
                body = {
                    "query":{
                        "bool":{
                            "must":query
                        }
                    },
                    "sort":order,
                    "size":size
                }
        )['hits']['hits']
    else:
        source = es_user_profile.search(\
                index = "weibo_user", doc_type="user", \
                body = {"query":{"match_all":{}}, "sort":order, "size":size})['hits']['hits']
    results = []
    for item in source:
        item['_source']['create_at'] = ts2datetime(item['_source']['create_at'])
        results.append(item['_source'])

    return json.dumps(results)

@mod.route('/get_sensitive_words/')
def ajax_get_sensitive_words():
    sensitive_words = R_ADMIN.hkeys("sensitive_words")
    return json.dumps(sensitive_words)
