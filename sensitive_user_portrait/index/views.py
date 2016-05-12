#-*- coding:utf-8 -*-

import json
import time
import datetime
from sensitive_user_portrait.extensions import user_datastore
from sensitive_user_portrait.time_utils import ts2datetime, ts2date
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect, make_response
from flask.ext.security import login_required

mod = Blueprint('sensitive', __name__, url_prefix='/index')


@mod.route('/')
def loading():
    return render_template('index.html')

@mod.route('/overview/')
@login_required
def overview():
    return render_template('index/overview.html')

@mod.route('/recommend_in/')
@login_required
def recommend_in():
    return render_template('index/recommend_in.html')
"""
@mod.route('/tag/')
def tag():
    return render_template('index/tag.html')
"""
@mod.route('/tag_search/')
@login_required
def tag_search():
    return render_template('index/search/tag_search.html')

@mod.route('/tag_manage/')
@login_required
def tag_manage():
    return render_template('index/tag_manage.html')
"""
@mod.route('/sensitive_words/')
def sensitive_words():
    return render_template('index/sensitive.html')
"""
@mod.route('/sensiwords_manage/')
@login_required
def sensiwords_manage():
    return render_template('index/sensiwords_manage.html')
    
@mod.route('/words_recommend/')
@login_required
def word_recommend():
    return render_template('index/words_recommend.html')

@mod.route('/group_identify/')
@login_required
def group():
    return render_template('index/group_identify.html')

'''
@mod.route('/group_results/')
def group_results():
    name = request.args.get('name', '')
    return render_template('index/group_results.html')
'''

@mod.route('/group_analysis/')
@login_required
def group_results():
    name = request.args.get('name', '')
    return render_template('index/group_analysis.html')

@mod.route('/group_task/')
@login_required
def group_task():
    return render_template('index/group_task.html')

@mod.route('/group_search/')
@login_required
def group_search():
    return render_template('index/search/group_search.html')

@mod.route('/search_portrait/')
@login_required
def search_portrait():
    return render_template('index/search/search_portrait.html')

@mod.route('/search_all/')
@login_required
def search_all():
    return render_template('index/search/search_all.html')

@mod.route('/search_context/')
@login_required
def search_context():
    return render_template('index/search/search_context.html')

@mod.route('/search_results/')
@login_required
def search_results():
    stype = request.args.get('stype','')
    uid = request.args.get('uid', '')
    uname = request.args.get('uname', '')
    location = request.args.get('location', '')
    activity_geo = request.args.get('activity_geo', '')
    adkeyword = request.args.get('adkeyword', '')
    hashtag = request.args.get('hashtag', '')
    psycho_status = request.args.get('psycho_status', '')
    psycho_feature = request.args.get('psycho_feature', '')
    domain = request.args.get('domain', '')
    topic = request.args.get('topic', '')
    tag = request.args.get('tag', '')

    if (stype == '1'):
        return render_template('index/search/search_results.html', uid=uid, uname=uname,\
                location=location, activity_geo=activity_geo, adkeyword=adkeyword, hashtag=hashtag, psycho_status=psycho_status,\
                psycho_feature=psycho_feature, domain=domain, topic=topic, tag=tag)
    elif (stype == '2'):
        return render_template('index/search/group_search_results.html', uid=uid, uname=uname,\
                location=location, activity_geo=activity_geo, adkeyword=adkeyword, hashtag=hashtag, psycho_status=psycho_status,\
                psycho_feature=psycho_feature, domain=domain, topic=topic, tag=tag)
    elif (stype == '3'):
        return render_template('index/search/tag_search_results.html', uid=uid, uname=uname,\
                location=location, activity_geo=activity_geo, adkeyword=adkeyword, hashtag=hashtag, psycho_status=psycho_status,\
                psycho_feature=psycho_feature, domain=domain, topic=topic, tag=tag)
    else:
        return render_template('index/search/search_results.html', uid=uid, uname=uname,\
                location=location, activity_geo=activity_geo, adkeyword=adkeyword, hashtag=hashtag, psycho_status=psycho_status,\
                psycho_feature=psycho_feature, domain=domain, topic=topic, tag=tag)

@mod.route('/text_search/')
@login_required
def text_search():
    words_list = request.args.get('words_list', '')
    return render_template('index/search/search_text_result.html', words_list=words_list)
@mod.route('/influence/')
@login_required
def influence():
    return render_template('index/influence.html')

@mod.route('/monitor/')
@login_required
def monitor():
    return render_template('index/monitor.html')

@mod.route('/connect/')
@login_required
def connect():
    return render_template('index/search_connect.html')

@mod.route('/portrait/')
@login_required
def portrait():
    return render_template('index/search_portrait.html')

@mod.route('/group_list/')
@login_required
def group_list():
    return render_template('index/group_list.html')

@mod.route('/personal/')
@login_required
def personal():
    uid = request.args.get('uid', '1215031834')
    uid = str(uid)
    return render_template('index/personal.html', uid=uid)
@mod.route('/personal_contect/')
@login_required
def personal_contect():
    return render_template('index/contact.html')
@mod.route('/sensitive_person/')
@login_required
def sensitive_person():
    uid = request.args.get('uid', '2697649164')
    uid = str(uid)
    return render_template('index/sensitive_person.html', uid=uid)

@mod.route('/contact/')
@login_required
def contact():
    uid = request.args.get('uid', '1022866242')
    return render_template('index/contact.html', uid=uid)

@mod.route('/sensing_weibo/')
@login_required
def sensing_weibo():
    return render_template('index/sensing_weibo.html')

@mod.route('/sensing_analysis/')
@login_required
def sensing_analysis():
    task_name = request.args.get('task_name','监督维权律师' )
    user = request.args.get('user', 'admin')
    ts = request.args.get('ts', '1378567800' )
    return render_template('index/sensing_analysis.html', task_name=task_name,user=user,ts=ts)

