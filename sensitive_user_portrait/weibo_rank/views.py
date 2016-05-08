#-*-coding: utf-8 -*-
import os
import time
import json
from Weibo_sort_interface import weibo_sort_interface
from sensitive_user_portrait.time_utils import ts2datetime
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from Offline_task import search_weibo_task , getResult , delOfflineTask

mod = Blueprint('weibo_rank', __name__, url_prefix='/weibo_rank')

@mod.route('/weibo_sort/', methods=['GET', 'POST'])
def weibo_sort():
    username = request.args.get('username', '')
    search_time = request.args.get('time', '') # 1 7 30
    sort_norm = request.args.get('sort_norm', '') # reposts_count comments_count
    sort_scope = request.args.get('sort_scope', '') # "all_limit_keyword" "all_nolimit"
    arg = request.args.get('arg', '')
    st = request.args.get('st', '') # "2013-09-01"
    et = request.args.get('et', '') # "2013-09-01"
    number = request.args.get('number', 100)
    task_number = request.args.get('task_number', 5)

    if arg :
        pass
    else :
        arg = None

    results = weibo_sort_interface(username, int(search_time), sort_scope, sort_norm, arg, st, et, task_number, number)

    return json.dumps(results)

@mod.route('/search_task/', methods=['GET', 'POST'])
def search_task():
    username = request.args.get('username', '')
    results = search_weibo_task(username)
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

