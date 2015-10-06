#-*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from imagine import imagine

mod = Blueprint('imagine', __name__, url_prefix='/imagine')

@mod.route('/')
def ajax_imagine():
    uid = request.args.get('uid', '') # uid
    query_keywords = request.args.get('keywords','') # query dict and corresponding weight
    keywords_list = query_keywords.split(',')
    query_weight = request.args.get('weight','')
    weight_list = query_weight.split(',')

    if len(keywords_list) != len(weight_list):
        return '0'

    query_fields_dict = {}
    for i in range(len(keywords_list)):
        query_fields_dict[keywords_list[i]] = int(weight_list[i])

    field = request.args.get('field', '')
    query_fields_dict['field'] = field

    size = request.args.get('size', 15)
    query_fields_dict['size'] = int(size)

    if uid and query_fields_dict:
        result = imagine(uid, query_fields_dict)
    if result:
        return json.dumps(result)

    return '0'


