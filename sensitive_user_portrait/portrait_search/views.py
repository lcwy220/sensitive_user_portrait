 #-*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from sensitive_user_portrait.global_utils import es_user_profile, es_sensitive_user_portrait, es_flow_text, es_tag
from sensitive_user_portrait.global_utils import portrait_index_name, portrait_index_type, flow_text_index_name_pre, \
                                                 flow_text_index_type, profile_index_name, profile_index_type
from sensitive_user_portrait.time_utils import ts2datetime, datetime2ts
from sensitive_user_portrait.parameter import RUN_TYPE
from utils import search_portrait,full_text_search

mod = Blueprint('search', __name__, url_prefix='/search')

@mod.route('/portrait_search/')
def ajax_portrait_search():
    stype = request.args.get('stype', '')
    result = {}
    query_data = {}
    query = []
    query_list = []
    condition_num = 0

    if stype:
        fuzz_item = ['uid', 'uname']
        item_data = request.args.get('term', '')
        for item in fuzz_item:
            if item_data:
                query_list.append({'wildcard':{item:'*'+item_data+'*'}})
                condition_num += 1
        query.append({'bool':{'should':query_list}})
    else:
        simple_item = ['uid', 'uname']
        fuzz_item = ['activity_geo', 'politics','keywords_string', 'hashtag','sensitive_words_string' ]
        multi_item = ['domain','topic_string']
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
                item_list = item_data.split(',')
                for term in item_list:
                    query.append({"terms":{term:item_list}})
                condition_num += 1
        # custom_attribute
        tag_items = request.args.get('tag', '')
        if tag_items != '':
            tag_item_list = tag_items.split(',')
            for tag_item in tag_item_list:
                attribute_name_value = tag_item.split(':')
                attribute_name = attribute_name_value[0]
                attribute_value = attribute_name_value[1]
                if attribute_name and attribute_value:
                    query.append({"term":{attribute_name:attribute_value}})
                    condition_num += 1

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
    if results:
        for item in results:
            sensitive_words.append(item['key'])

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

