#-*- coding:utf-8 -*-

import json
import time
import datetime
from sensitive_user_portrait.time_utils import ts2datetime, ts2date
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect, make_response


mod = Blueprint('sensitive', __name__, url_prefix='/index')


@mod.route('/')
def loading():

    return render_template('index.html')

@mod.route('/overview/')
def overview():
    return render_template('index/overview.html')

@mod.route('/recommend_in/')
def recommend_in():
    return render_template('index/recommend_in.html')
"""
@mod.route('/tag/')
def tag():
    return render_template('index/tag.html')
"""
@mod.route('/tag_search/')
def tag_search():
    return render_template('index/search/tag_search.html')

@mod.route('/tag_manage/')
def tag_manage():
    return render_template('index/tag_manage.html')
"""
@mod.route('/sensitive_words/')
def sensitive_words():
    return render_template('index/sensitive.html')
"""
@mod.route('/sensiwords_manage/')
def sensiwords_manage():
    return render_template('index/sensiwords_manage.html')
    
@mod.route('/words_recommend/')
def word_recommend():
    return render_template('index/words_recommend.html')

@mod.route('/group_identify/')
def group():
    return render_template('index/group_identify.html')

@mod.route('/group_results/')
def group_results():
    name = request.args.get('name', '')
    return render_template('index/group_results.html')

@mod.route('/group_task/')
def group_task():
    return render_template('index/group_task.html')

@mod.route('/group_search/')
def group_search():
    return render_template('index/search/group_search.html')

@mod.route('/search_portrait/')
def search_portrait():
    return render_template('index/search/search_portrait.html')

@mod.route('/search_all/')
def search_all():
    return render_template('index/search/search_all.html')

@mod.route('/search_results/')
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
def text_search():
    words_list = request.args.get('words_list', '')
    return render_template('index/search/search_text_result.html', words_list=words_list)
@mod.route('/influence/')
def influence():
    return render_template('index/influence.html')

@mod.route('/monitor/')
def monitor():
    return render_template('index/monitor.html')

@mod.route('/connect/')
def connect():
    return render_template('index/search_connect.html')

@mod.route('/portrait/')
def portrait():
    return render_template('index/search_portrait.html')

@mod.route('/group_list/')
def group_list():
    return render_template('index/group_list.html')

@mod.route('/personal/')
def personal():
    uid = request.args.get('uid', '1215031834')
    uid = str(uid)
    return render_template('index/personal.html', uid=uid)
@mod.route('/personal_contect/')
def personal_contect():
    return render_template('index/contact.html')
@mod.route('/sensitive_person/')
def sensitive_person():
    uid = request.args.get('uid', '2697649164')
    uid = str(uid)
    return render_template('index/sensitive_person.html', uid=uid)

@mod.route('/contact/')
def contact():
    uid = request.args.get('uid', '1022866242')
    return render_template('index/contact.html', uid=uid)

@mod.route('/sensing_weibo/')
def sensing_weibo():
    return render_template('index/sensing_weibo.html')

@mod.route('/sensing_analysis/')
def sensing_analysis():
    task_name = request.args.get('task_name','监督维权律师' )
    user = request.args.get('user', 'admin')
    ts = request.args.get('ts', '1378567800' )
    return render_template('index/sensing_analysis.html', task_name=task_name,user=user,ts=ts)

