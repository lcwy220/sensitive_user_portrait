#-*- coding: UTF-8 -*-

import os
import time
import sys
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from sensitive_user_portrait.global_utils import ES_CLUSTER_FLOW1 as es
from influence_description import influence_description

portrait_index = "copy_user_portrait" # user_portrait_database
portrait_type = "user"

mod = Blueprint('influence_application', __name__, url_prefix='/influence_application')

@mod.route('/search_domain_influence/')
def ajax_search_influence():
    date = request.args.get('date', '') # '2013-09-01'
    number = request.args.get('number', 100) # "100"
    domain = request.args.get('domain', 0) # 0: all active rank, 1: portrait active rank

    index_name = str(date).replace('-','')
    number = int(number)
    domain = int(domain)

    if not index_name:
        return 0

