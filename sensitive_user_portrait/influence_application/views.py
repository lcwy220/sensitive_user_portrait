#-*- coding: UTF-8 -*-

import os
import time
import sys
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from sensitive_user_portrait.global_utils import ES_CLUSTER_FLOW1 as es
from influence_description import influence_description
from utils import test_influence_rank, influence_distribute, search_domain

portrait_index = "copy_user_portrait" # user_portrait_database
portrait_type = "user"

mod = Blueprint('influence_application', __name__, url_prefix='/influence_application')

@mod.route('/search_domain_influence/')
def ajax_search_influence():
    date = request.args.get('date', '') # '2013-09-01'
    number = request.args.get('number', 100) # "100"
    domain = request.args.get('domain', '') # 维权律师
    order = request.args.get('order', '') # 1: influence, 2: retweeted, 3, comment, 4: retweeted_brust. 5: comment_brust

    index_name = str(date).replace('-','')
    number = int(number)
    domain = domain.encode('utf-8', 'ignore')
    order = int(order)
    if not index_name:
        return '0'
    results = test_influence_rank(domain, index_name, order)
    return json.dumps(results)


@mod.route('/influence_distribution/')
def ajax_influence_distribution():
    results = []
    results = influence_distribute()
    return json.dumps(results)


