# -*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from sensitive_user_portrait.global_utils import es_sensitive_user_portrait as es
from sensitive_user_portrait.global_utils import es_user_profile
from sensitive_user_portrait.global_utils import R_RECOMMENTATION as r
from utils import search_attribute_portrait,search_portrait
from utils import extract_uname, search_sensitive_text, sensitive_attribute
from utils import user_sentiment_trend, sort_sensitive_words, search_sensitive_text, sort_sensitive_text, sensitive_attribute, search_full_text

category = ['politics', 'military', 'law', 'ideology', 'democracy']

mod = Blueprint('attribute', __name__, url_prefix='/attribute')

@mod.route('/portrait_attribute/')
def ajax_portrait_attribute():
    uid = request.args.get('uid', '')
    uid = str(uid)
    results = search_attribute_portrait(uid)
    if results:
        return json.dumps(results)
    else:
        return '0'

@mod.route('/portrait_sensitive_attribute/')
def ajax_portrait_sensitive_attribute():
    uid = request.args.get('uid', '')
    uid = str(uid)
    results = sensitive_attribute(uid)
    if results:
        return json.dumps(results)
    else:
        return '0'

# weibo text of every day
@mod.route('/detail_weibo_text/')
def ajax_detail_weibo_text():
    uid = str(request.args.get('uid', ''))
    date = request.args.get('date', '') # date: 2013-09-01
    results = []
    results = search_full_text(uid, date)
    return json.dumps(results)


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
        # print 'tag_term_list:', tag_item_list
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
    # print 'condition_num, query:', condition_num, query
    result = search_portrait(condition_num, query, sort, size)
    return json.dumps(result)

@mod.route('/sort_sensitive_words/')
def ajax_sort_sensitive_words():
    level_order = request.args.get('level', '') # 0:all, 1:level 1, 2:level2, 3:level3
    category_order =  request.args.get('category', '')
    uid = request.args.get('uid', '')
    words_dict = es.get(index='sensitive_user_portrait', doc_type='user', id=uid)['_source']['sensitive_words_dict']
    words_dict = json.loads(words_dict)
    all_words_dict = dict()
    for v in words_dict.values():
        for key in v:
            if all_words_dict.has_key(key):
                all_words_dict[key] += v[key]
            else:
                all_words_dict[key] = v[key]
    sorted_words = sorted(all_words_dict.items(), key = lambda x:x[1], reverse=True)
    new_words_list = sort_sensitive_words(sorted_words)
    print new_words_list
    if order == 'level':
        level_1 = []
        level_2 = []
        level_3 = []
        for item in new_words_list:
            if int(item[2]) == 1:
                level_1.append(item)
            elif int(item[2]) == 2:
                level_2.append(item)
            elif int(item[2]) == 3:
                level_3.append(item)
        new_level = []
        new_level.extend(level_3)
        new_level.extend(level_2)
        new_level.extend(level_1)
        return json.dumps(new_level)
    elif order == 'category':
        new_level = [[], [], [], [], []]
        for item in new_words_list:
            index = category.index(item[3])
            new_level[index].append(item)
        return json.dumps(new_level)
    else:
        return '0'


@mod.route('/sort_sensitive_text/')
def ajax_sort_sensitive_text():
    weibo_category = request.args.get('weibo_category', '') # 0: all, 1: origin weibo, 2: retweeted weibo
    sort = request.args.get('sort', '') # 0:timestamp, 1: retweeted number, 2: comment number
    uid = request.args.get('uid', '')
    text_all = sort_sensitive_text(uid)
    sorted_text_list = sorted(text_all, key=lambda x:x[0], reverse=True)
    text_list = []
    print weibo_category
    for item in sorted_text_list:
        if int(weibo_category) == 1: # origin weibo sorted
            if int(item[6]) == 1:
                text_list.append(item)
        elif int(weibo_category) == 2:
            if int(item[6]) == 2:
                text_list.append(item)
        else:
            pass
    if int(weibo_category) == 0:
        text_list = sorted_text_list

    if int(sort) == 0:
        return_list = sorted(text_list, key=lambda x:x[0], reverse=True)
    elif int(sort) == 1:
        return_list = sorted(text_list, key=lambda x:x[-2], reverse=True)
    elif int(sort) == 2:
        return_list = sorted(text_list, key=lambda x:x[-1], reverse=True)
    else:
        return_list = []

    return json.dumps(return_list)

