#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from sensitive_user_portrait.time_utils import ts2datetime
from User_sort_interface import user_sort_interface
from Offline_task import search_user_task , getResult , delOfflineTask, sort_task
from temporal_rank import get_temporal_rank

mod = Blueprint('user_rank', __name__, url_prefix='/user_rank')

@mod.route('/user_sort/', methods=['GET', 'POST'])
def user_sort():
    username = request.args.get('username', '')
    search_time = request.args.get('time', '') # 1 7 30
    sort_norm = request.args.get('sort_norm', '') # bci fans
    print "---------------------------", sort_norm
    sort_scope = request.args.get('sort_scope', '') # "all_limit_keyword" "all_nolimit" 'in_limit_keyword' 'in_limit_hashtag'
    arg = request.args.get('arg', '')
    st = request.args.get('st', '') # "2013-09-01"
    et = request.args.get('et', '') # "2013-09-01"
    isall = request.args.get('all','') # True or False
    number = request.args.get('number', 100)
    task_number = request.args.get('task_number', 10)
    _all = True
    if isall == 'True':
        _all = True
    else :
        _all = False
    if arg :
        pass
    else :
        arg = None
    print username, search_time, sort_norm, sort_scope, arg
    results = user_sort_interface(username,int(search_time),sort_scope,sort_norm,arg,st,et,_all,int(task_number), int(number))
    return json.dumps(results)

@mod.route('/search_task/', methods=['GET', 'POST'])
def search_task():
    username = request.args.get('username', '')
    results = search_user_task(username)
    return json.dumps(results)

@mod.route('/get_result/' , methods=['GET','POST'])
def get_result():
    search_id = request.args.get('search_id','')
    results = getResult(search_id)
    return json.dumps(results)

@mod.route('/delete_task/' , methods =['GET','POST'])
def delete_task():
    search_id = request.args.get('search_id','')
    result = {}
    result['flag'] = delOfflineTask(search_id)
    return json.dumps(result)


@mod.route('/temporal_rank/')
def temporal_rank():
    task_type = request.args.get("task_type", "0")
    sort = request.args.get("sort", "retweeted") # comment
    number = request.args.get("number", 100)
    results = []
    task_type = int(task_type)
    results = get_temporal_rank(task_type, sort,number)

    return json.dumps(results)

@mod.route('/task_sort/')
def ajax_task_sort():
    results = []
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    user = request.args.get('user', '')
    keyword = request.args.get("keyword", "") # 逗号分隔
    status = request.args.get("status", 2) # 2 for all, no limit
    start_time = request.args.get("start_time", "")
    end_time = request.args.get("end_time", now_date)
    submit_time = request.args.get('submit_time', "")
    status = int(status)
    
    #if user:
    results = sort_task(user, keyword, status, start_time, end_time, submit_time)

    return json.dumps(results)


