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

@mod.route('/sensitive_words/')
def sensitive_words():
    return render_template('index/sensitive.html')

@mod.route('/group/')
def group():
    return render_template('index/group.html')

@mod.route('/search/')
def search():
    return render_template('index/search.html')

@mod.route('/influence/')
def influence():
    return render_template('index/influence.html')

@mod.route('/monitor/')
def monitor():
    return render_template('index/monitor.html')

@mod.route('/contrast/')
def contrast():
    return render_template('index/contrast.html')

@mod.route('/group_task/')
def group_task():
    return render_template('index/group_task.html')
