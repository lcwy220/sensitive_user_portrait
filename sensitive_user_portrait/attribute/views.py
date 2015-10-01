# -*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from sensitive_user_portrait.global_utils import es_sensitive_user_portrait as es
from sensitive_user_portrait.global_utils import es_user_profile
from utils import search_attribute_portrait,search_mention, search_portrait
from utils import extract_uname, search_sensitive_text

mod = Blueprint('attribute', __name__, url_prefix='/attribute')

@mod.route('/portrait_attribute/')
def ajax_portrait_attribute():
    uid = request.args.get('uid', '')
    uid = str(uid)
    u_list = []
    #results = search_attribute_portrait(uid)
    results = search_sensitive_text(uid)
    if results:
        for item in results:
            u_list.append(extract_uname(item['_source']['text']))
            u_list.append(sentiment(item['_source']['text']))
    if results:
        return json.dumps(u_list)
    else:
        return '0'

@mod.route('/mention/')
def ajax_mention():
    uid = request.args.get('uid', '')
    uid = str(uid)
    now_ts = time.time()

    results = search_mention(uid)
    if results:
        return json.dumps(results)
    else:
        return '0'


@mod.route('/search_portrait/')
def ajax_search_portrait():
    query_list = []
    condition_num = 0
    query = []
    result = {}
    query_date = {}

    shift_dict = {'activity_geo':'geo_string', 'keywords':'keywords_string', 'hashtag':'hashtag_string', \
            'sensitive_words':'sensitive_words_string', 'sensitive_geo_activity':'sensitive_geo_string', \
            'sensitive_hashtag_string':'sensitive_hashtag_string', 'topic':'topic_string'}

    fuzz_item = ['uid', 'uname', 'location', 'activity_geo', 'keywords', 'hashtag']
    sensitive_item = ['sensitive_words', 'sensitive_geo_activity', 'sensitive_hashtag']
    select_item = ['gender', 'verified', 'psycho_feature', 'psycho_status']
    range_item = ['fansnum', 'statusnum', 'friendsnum', 'importance', 'activeness', 'influence']
    multi_item = ['topic', 'domain']
    for item in fuzz_item:
        item_data = request.args.get(item, '')
        if item_data:
            if shift_dict.has_key(item):
                query.append({'wildcard':{shift_dict[item]:'*'+item_data+'*'}})
            else:
                query.append({'wildcard':{item:'*'+item_data+'*'}})
            condition_num += 1
    for item in select_item:
        item_data = request.args.get(item, '')
        if item_data:
            if shift_dict.has_key(item):
                query.append({'wildcard':{shift_dict[item]:'*'+item_data+'*'}})
            else:
                query.append({'wildcard':{item:'*'+item_data+'*'}})
            condition_num += 1
    for item in sensitive_item:
        item_data = request.args.get(item, '')
        if item_data:
            if shift_dict.has_key(item):
                query.append({'wildcard':{shift_dict[item]:'*'+item_data+'*'}})
            else:
                query.append({'wildcard':{item:'*'+item_data+'*'}})
            condition_num += 1
    '''
    if custom_attribute_list: 
        for custom_tag in custom_attribute_list:
            item_data = request.args.get(custom_tag, '')
            query.append({'wildcard':{custom_tag:'*'+item_data+'*'}})
            condition_num += 1
    '''
    tag_items = request.args.get('tag', '')
    if tag_items:
        tag_item_list = tag_items.split(',')
        print 'tag_term_list:', tag_item_list
        for tag_item in tag_item_list:
            attribute_name_value = tag_item.split(':')
            attribute_name = attribute_name_value[0]
            attribute_value = attribute_name_value[1]
            if attribute_name and attribute_value:
                query.append({'wildcard':{attribute_name:'*'+attribute_value+'*'}})
                condition_num += 1

    for item in multi_item:
        nest_body = {}
        nest_body_list = []
        item_data = request.args.get(item, '')
        if item == 'topic':
            item = 'topic_string'
        if item_data:
            term_list = item_data.split(',')
            for term in term_list:
                nest_body_list.append({'match':{item: term}})
            condition_num += 1
            query.append({'bool':{'should':nest_body_list}})

    # size = request.args.get('size', 1000)
    size = 1000
    # sort = request.args.get('sort', 'influence')
    sort= '_score'
    print 'condition_num, query:', condition_num, query
    result = search_portrait(condition_num, query, sort, size)
    return json.dumps(result)


