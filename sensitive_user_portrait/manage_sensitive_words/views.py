# -*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from sensitive_user_portrait.global_utils import R_RECOMMENTATION as r
from sensitive_user_portrait.time_utils import datetime2ts, ts2datetime
from utils import lastest_identify_in, self_delete, self_add_in, search_sensitive_words, identify_in, recommend_new_words
mod = Blueprint('manage_sensitive_words', __name__, url_prefix='/manage_sensitive_words')

@mod.route('/recommend_new_words/')
def ajax_recommend_new_words():
    date_list = request.args.get('date_list', '') # 2013-09-01, 2013-09-02
    date_list = date_list.split(',')
    if date_list:
        results = recommend_new_words(date_list)
        return json.dumps(results)
    else:
        return '0'


@mod.route('/identify_in/')
def ajax_identify_in():
    date = request.args.get('date', '') # 
    words_list = request.args.get('words_list', '') # ,
    level_list = request.args.get('level_list', '') # ,
    category_list = request.args.get('category_list', '') # ,

    words_list = words_list.split(',')
    level_list = level_list.split(',')
    category_list = category_list.split(',')
    date = date.replace('-', '')

    total = []
    for i in range(len(words_list)):
        detail = []
        detail.append(words_list[i].encode('utf-8', 'ignore'))
        detail.append(level_list[i].encode('utf-8', 'ignore'))
        detail.append(category_list[i].encode('utf-8', 'ignore'))
        total.append(detail)
    results = identify_in(date, total)

    return results

@mod.route('/search_sensitive_words/')
def ajax_search_sensitive_words():
    state = request.args.get('state', '')
    if state:
        results = search_sensitive_words(state)
        return json.dumps(results)
    else:
        return '0'

@mod.route('/self_add_in/')
def ajax_self_add_in():
    date = request.args.get('date', '')
    date = date.replace('-','')
    word = request.args.get('word', '')
    word = word.encode('utf-8', 'ignore')
    level = request.args.get('level', '')
    category = request.args.get('category', '')
    category = category.encode('utf-8', 'ignore')
    result = '0'
    if date and word and level and category:
        result = self_add_in(date, word, level, category)

    return result

@mod.route('/self_delete/')
def ajax_self_delete():
    word = request.args.get('word', '')
    word = word.encode('utf-8', 'ignore')
    result = '0'
    if word:
        result = self_delete(word)
    return result

@mod.route('/lastest_identify_in/')
def ajax_lastest_identify_in():
    results = lastest_identify_in()
    if results:
        return json.dumps(results)
    else:
        return '0'

