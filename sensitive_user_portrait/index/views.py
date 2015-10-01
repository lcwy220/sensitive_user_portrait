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

@mod.route('/tag/')
def tag():
    return render_template('index/tag.html')

@mod.route('/tag_search/')
def tag_search():
    return render_template('index/search/tag_search.html')

@mod.route('/tag_manage/')
def tag_manage():
    return render_template('index/tag_manage.html')

@mod.route('/sensitive_words/')
def sensitive_words():
    return render_template('index/sensitive.html')

@mod.route('/group/')
def group():
    return render_template('index/group.html')

@mod.route('/group_task/')
def group_task():
    return render_template('index/group_task.html')

@mod.route('/group_search/')
def group_search():
    return render_template('index/search/group_search.html')

@mod.route('/search/')
def search():
    return render_template('index/search/search.html')

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

@mod.route('/influence/')
def influence():
    return render_template('index/influence.html')

@mod.route('/monitor/')
def monitor():
    return render_template('index/monitor.html')

@mod.route('/contrast/')
def contrast():
    return render_template('index/contrast.html')


@mod.route('/group_analysis/')
def group_analysis():
    return render_template('index/group_analysis.html')

@mod.route('/personal/')
def personal():
    return render_template('index/personal.html')






