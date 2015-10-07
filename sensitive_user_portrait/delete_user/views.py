#-*- coding:utf-8 -*-

import os
import json
import time
import redis
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from sensitive_user_portrait.global_utils import R_RECOMMENTATION as r
from sensitive_user_portrait.time_utils import datetime2ts
from utils import get_user_info

mod = Blueprint('delete_user', __name__, url_prefix='/delete_user')

@mod.route('/delete_user/')
def ajax_delete_user():
    date = request.args.get('date', '') # '2013-09-01'
    date = str(date).replace('-', '')
    uid_list = request.args.get('uid_list', '') # uid_list, 12345,123456,
    delete_list = str(uid_list).split(',')

    if date and delete_list:
        temp = r.hget('delete_user', date)
        if temp:
            exist_data = json.loads(temp)
            delete_list.extend(exist_data)
        r.hset('delete_user', date, json.dumps(delete_list))
        return '1'
    else:
        return '0'

@mod.route('/history_delete/')
def ajax_history_delete():
    date = request.args.get('date', '') # '2013-09-01'
    date = str(date).replace('-', '')
    search_all  = request.args.get('show_all', '') # return all
    uid_list = []
    if not search_all:
        temp = r.hget('delete_user', date)
        if temp:
            results = get_user_info(json.loads(temp))
            return json.dumps(results)
    else:
        all_temp = r.hgetall('delete_user')
        if all_temp:
            temp_list = all_temp.values()
            for item in temp_list:
                uid_list.extend(json.loads(item))
            results = get_user_info(uid_list)
            return json.dumps(results)
    return '0'

@mod.route('/cancel_delete/')
def ajax_cancel_delete():
    uid_list = request.args.get('uid_list', '')
    date = request.args.get('date', '')
    if not uid_list or not date:
        return '0'
    else:
        uid_list = str(uid_list).split(',')
        date = str(date).replace('-', '')
        delete_list = json.loads(r.hget('delete_user', date))
        revise_list = set(delete_list) - set(uid_list)
        if revise_list:
            r.hset('delete_user', date, json.dumps(list(revise_list)))
        else:
            r.hdel('delete_user', date)
        return '1'


