#-*- coding:utf-8 -*-

import os
import redis
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from utils import recommend_in_sensitive, recommend_in_top_influence, influence_recommentation_more_information
from utils import sensitive_recommentation_more_information, identify_in, show_in_history
from sensitive_user_portrait.global_utils import R_RECOMMENTATION as r
from sensitive_user_portrait.time_utils import datetime2ts, ts2datetime


mod = Blueprint('recommentation', __name__, url_prefix='/recommentation')


# sensitive weibo user recommendtation
@mod.route('/show_sensitive_list/')
def ajax_recommentation_in_sensitive_list():
    date = request.args.get('date', '') # 2013-09-01
    """
    ts = datetime2ts(ts2datetime(time.time()-6*24*3600))
    input_ts = datetime2ts(date)
    if input_ts < ts:
        return '0'
    else:
        results = recommend_in_sensitive(date)
    """
    results = recommend_in_sensitive(date)
    if results:
        return json.dumps(results)
    else:
        return json.dumps([])


# top influence user recommentation
@mod.route('/show_influence_list/')
def ajax_recommentation_in_influence_list():
    date = request.args.get('date', '') # 2013-09-01
    '''
    ts = datetime2ts(ts2datetime(time.time()-6*24*3600))
    input_ts = datetime2ts(date)
    if input_ts < ts:
        return '0'
    else:
        results = recommend_in_top_influence(date)
    '''
    results = recommend_in_top_influence(date)
    if results:
        return json.dumps(results)
    else:
        return json.dumps([])


# top influence user show more information
@mod.route('/influence_show_in_more/')
def ajax_influence_recommentation_in_more():
    uid = request.args.get('uid','')
    results = influence_recommentation_more_information(uid)
    if results:
        return json.dumps(results)
    else:
        return json.dumps([])


# sensitive user show more info
@mod.route('/sensitive_show_in_more/')
def ajax_sensitive_recommentation_in_more():
    uid = request.args.get('uid','')
    results = sensitive_recommentation_more_information(uid)
    if results:
        return json.dumps(results)
    else:
        return json.dumps([])

# identify in
@mod.route('/identify_in/')
def ajax_identify_in():
    date = request.args.get('date','') # date: 2013-09-01, recommend date
    date = date.replace('-','')
    uid_list = request.args.get('uid_list','') # 123,456,789
    uid_list = uid_list.split(',')
    status = request.args.get('status','') # 1: compute now, 2: appointed compute
    source = request.args.get('source','') # 1: sensitive user, 2: influence user
    data = []
    if date and uid_list:
        for uid in uid_list:
            data.append([date, uid, status, source])
        result = identify_in(data)
    else:
        result = []
    return json.dumps(result)


# show sensitive user history in
@mod.route('/show_sensitive_history_in/')
def ajax_show_sensitive_history_in():
    results = []
    now_date = ts2datetime(time.time())
    date = request.args.get('date', now_date) # in date:2013-09-01
    if str(date) == "all":
        ts = time.time()
        now_ts = datetime2ts('2013-09-07')
        for i in range(7):
            ts = now_ts - i*24*3600
            date = ts2datetime(ts)
            date = str(date).replace('-', '')
            temp = show_in_history(date, 1)
            results.extend(temp)
    else:
        date = str(date).replace('-','')
        results = show_in_history(date, 1) # history in, include status
    if results:
        return json.dumps(results)
    else:
        return json.dumps([])

#show influence user history in
@mod.route('/show_influence_history_in/')
def ajax_show_influence_history_in():
    results = []
    now_date = ts2datetime(time.time())
    date = request.args.get('date', now_date)
    if str(date) == "all":
        ts = time.time()
        now_ts = datetime2ts('2013-09-07')
        for i in range(7):
            ts = now_ts - i*24*3600
            date = ts2datetime(ts)
            date = str(date).replace('-', '')
            temp = show_in_history(date, 1)
            results.extend(temp)
    else:
        date = str(date).replace('-','')
        results = show_in_history(date, 0) # history in, include status
    if results:
        return json.dumps(results)
    else:
        return json.dumps([])

