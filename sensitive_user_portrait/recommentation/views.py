#-*- coding:utf-8 -*-

import os
import redis
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from utils import recommend_in_sensitive, recommend_in_top_influence, recommentation_more_information
from sensitive_user_portrait.global_utils import R_RECOMMENTATION as r
from sensitive_user_portrait.time_utils import datetime2ts, ts2datetime


mod = Blueprint('recommentation', __name__, url_prefix='/recommentation')


# sensitive weibo user recommendtation
@mod.route('/show_in/sensitive_list')
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

    return json.dumps(results)


# top influence user recommentation
@mod.route('show_in/influence_list')
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

    return json.dumps(results)


# show more information
@mod.route('/show_in_more/')
def ajax_recommentation_in_more():
    uid = request.args.get('uid','')
    results = recommentation_more_information(uid)
    return json.dumps(results)



