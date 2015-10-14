#-*- coding:utf-8 -*-

import os
import time
import json
from werkzeug import secure_filename
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect, send_from_directory
from utils import submit_task, search_task, get_group_results, get_group_list, delete_group_results
#track utils
from track_utils import submit_track_task, search_track_task,\
                        end_track_task, delete_track_task
from track_result_utils import get_track_result, get_count_weibo, get_sentiment_weibo, \
                               get_sensitive_word, get_geo_user, get_geo_weibo, \
                               get_inner_top_weibo

from sensitive_user_portrait.global_config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from sensitive_user_portrait.search_user_profile import es_get_source
from sensitive_user_portrait.time_utils import ts2datetime, datetime2ts, ts2date, date2ts

mod = Blueprint('group', __name__, url_prefix='/group')

# use to upload file
@mod.route('/upload_file/', methods=['GET', 'POST'])
def upload_file():
    upload_data = request.form['upload_data']
    task_name = request.form['task_name']
    state = request.form['state']
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    line_list = upload_data.split('\n')
    input_data = {}
    input_data['submit_date'] = now_date
    input_data['task_name'] = task_name
    input_data['state'] = state
    uid_list = []
    for line in line_list:
        uid = line[:10]
        if len(uid)==10:
            uid_list.append(uid)
            #print 'uid:', uid
    #print 'len uid list:', len(uid_list)
    input_data['uid_list'] = uid_list
    status = submit_task(input_data)
    return json.dumps(status)


# submit group analysis task and save to redis as lists
# submit group task: task name should be unique
# input_data is dict ---two types
# one type: {'submit_date':x, 'state': x, 'uid_list':[],'task_name':x}
# two type: {'submit_date':x, 'state': x, 'task_name':x, 'uid_file':filename}
@mod.route('/submit_task/',methods=['GET', 'POST'])
def ajax_submit_task():
    input_data = dict()
    """
    input_data['task_name'] = request.args.get('task_name', '')
    input_data['uid_list'] = request.args.get('uid_list', '') # uid_list=[uid1, uid2]
    input_data['submit_date'] = request.args.get('submit_date', '')
    input_data['state'] = request.args.get('state', '')
    """
    input_data = request.get_json()
    #print input_data, type(input_data)
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    input_data['submit_date'] = now_date
    status = submit_task(input_data)
    return json.dumps(status)

# show the group task table
@mod.route('/show_task/')
def ajax_show_task():
    results = {}
    task_name = request.args.get('task_name', '')
    #print 'task_name:', task_name
    submit_date = request.args.get('submit_date', '')
    state = request.args.get('state', '')
    status = request.args.get('status', '')
    results = search_task(task_name, submit_date, state, status)
    print 'lem results:', len(results)
    return json.dumps(results)


# show the group analysis result---different module
@mod.route('/show_group_result/')
def ajax_show_group_result_basic():
    results = {}
    task_name = request.args.get('task_name', '')
    module = request.args.get('module', 'basic')
    results = get_group_results(task_name, module)
    #print 'result:', results
    return json.dumps(results)

#show the group member list
@mod.route('/show_group_list/')
def sjax_show_group_list():
    results = []
    task_name = request.args.get('task_name', '')
    results = get_group_list(task_name)
    return json.dumps(results)

# delete the group task
@mod.route('/delete_group_task/')
def ajax_delete_group_task():
    results = {}
    task_name = request.args.get('task_name', '')
    results = delete_group_results(task_name)
    return json.dumps(results)

'''
below: track a group analysis result
deal procession:
work1: submit track a group analysis task
work2: search the track task-----a table
work3: look the track results
work4: end a track task
work5: delete a track task results
add a field to mark the group analysis task is track or once
add track group analysis information to overview
'''

# submit task to track a group analysis result
#input_data = 'task_name', 'uid_list', 'state'
@mod.route('/upload_track_task/', methods=['GET', 'POST'])
def ajax_upload_track_file():
    results = {}
    upload_data = request.form['upload_data']
    task_name = request.form['task_name']
    state = request.args.form['state']
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    now_date_ts = datetime2ts(now_date)
    time_segment = int((now_ts - now_Date_ts) / 900) + 1
    trans_ts = now_date_ts + time_segment * 900
    line_list = upload_data.split('\n')
    input_data = {}
    #submit task and start time is 15min multiple
    input_data['submit_date'] = trans_ts
    input_data['task_name'] = task_name
    uid_list = []
    for line in line_list:
        uid = line[:10]
        if len(uid)==10:
            uid_list.append(uid)
    input_data['uid_list'] = uid_list
    input_data['status'] = 1 # status show the track task is doing or end; doing 1, end 0
    input_data['count'] = len(uid_list)
    status = submit_track_task(input_data)
    return json.dumps(status)

# submit_task
@mod.route('/submit_track_task/', methods=['GET', 'POST'])
def ajax_submit_track_task():
    input_data = dict()
    #input_data = request.get_json()
    # test
    input_data = {'task_name':'testtask', 'state':'it is a test', 'uid_list':['1311967407', '1671386130', '1653255165']}
    #input_data = {'task_name': 'testtask2', 'state': 'it is a test', \
    #        'uid_list':['3270699555', '3199485481', '1736407257', '1471234522', '1158518402', '1688547585', '1947335820', '3200285974']}
    '''
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    now_date_ts = datetime2ts(now_date)
    timesegment = int((now_ts - now_date_ts) / 900) + 1
    trans_ts = now_date_ts + timesegment * 900
    trans_date = ts2date(trans_date)
    input_data['submit_date'] = trans_date
    '''
    #test
    input_data['submit_date'] = '2013-09-01 00:00:00'
    input_data['status'] = 1 # show track task is doing; doing 1, end 0
    len_uid_list = len(input_data['uid_list'])
    input_data['count'] = len_uid_list
    status = submit_track_task(input_data)
    return json.dumps(status)


# search track task
@mod.route('/search_track_task/')
def ajax_search_track_task():
    results = {}
    task_name = request.args.get('task_name', '')
    submit_date = request.args.get('submit_date', '')
    state = request.args.get('state', '')
    status = request.args.get('status', '') # doing 1; end 0
    results = search_track_task(task_name, submit_date, state, status)
    return json.dumps(results)

# get the track results
@mod.route('/track_task_results/')
def ajax_get_track_results():
    results = {}
    task_name = request.args.get('task_name', '')
    module = request.args.get('module', 'basic') #module=basic/comment_retweet/network
    results = get_track_result(task_name, module)
    return json.dumps(results)

# end a track task
@mod.route('/end_track_task/')
def ajax_end_track_task():
    results = {}
    task_name = request.args.get('task_name', '')
    status = end_track_task(task_name)
    return json.dumps(status)

# delete a track task results
@mod.route('/delete_track_results/')
def ajax_delete_track_tresults():
    results = {}
    task_name = request.args.get('task_name', '')
    status = delete_track_task(task_name)
    return json.dumps(status)

# show weibo when click count node
@mod.route('/get_count_weibo/')
def ajax_get_node_weibo():
    results = {}
    task_name = request.args.get('task_name', '')
    sensitive_status = request.args.get('sensitive_status', '') # 0 unsensitive 1 sensitive
    sensitive_status = int(sensitive_status)
    timestamp = request.args.get('timestamp', '')
    timestamp = int(timestamp)
    results = get_count_weibo(task_name, sensitive_status, timestamp)
    return json.dumps(results)

# show weibo when click sentiment node
@mod.route('/get_sentiment_weibo/')
def ajax_get_sentiment_weibo():
    results = {}
    task_name = request.args.get('task_name', '')
    sensitive_status = request.args.get('sensitive_status', '') # 0 unsensitive 1 sensitive
    sensitive_status = int(sensitive_status)
    sentiment = request.args.get('sentiment', '') # sentiment 126, 127, 128, 129, 130
    timestamp = request.args.get('timestamp', '')
    timestamp = int(timestamp)
    results = get_sentiment_weibo(task_name, sentiment, timestamp)
    return json.dumps(results)

# show sensitive_word when click sensitive score
@mod.route('/get_sensitive_word/')
def ajax_get_sensitive_word():
    results = {}
    task_name = request.args.get('task_name', '')
    timestamp = request.args.get('timestamp', '')
    timestamp = int(timestamp)
    results = get_sensitive_word(task_name, timestamp)
    return json.dumps(results)

# show user when click geo
@mod.route('/get_geo_user/')
def ajax_get_geo_user():
    results = {}
    task_name = request.args.get('task_name', '')
    geo = request.args.get('geo', '')
    timestamp = request.args.get('timestamp', '')
    timestamp = int(timestamp)
    results = get_geo_user(task_name, geo, timestamp)
    return json.dumps(results)

# show weibo when click geo
@mod.route('/get_geo_weibo/')
def ajax_get_geo_ewibo():
    results = {}
    task_name = request.args.get('task_name', '')
    geo = request.args.get('geo', '')
    timestamp = request.args.get('timestamp', '')
    timestamp = int(timestamp)
    results = get_geo_weibo(task_name, geo, timestamp)
    return json.dumps(results)

# show weibo when click inner retweet top
@mod.route('/get_inner_top_weibo/')
def ajax_get_inner_top_weibo():
    result = {}
    task_name = request.args.get('task_name', '')
    date = request.args.get('date', '') # date = '2013-09-01'
    uid = requesta.args.get('uid', '')
    result = get_inner_top_weibo(task_name, date, uid)
    return json.dumps(result)
