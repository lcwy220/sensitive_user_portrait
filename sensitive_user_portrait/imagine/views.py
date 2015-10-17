#-*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from imagine import imagine

mod = Blueprint('imagine', __name__, url_prefix='/imagine')
shift_dict = {"sensitive_words": "sensitive_words_string", "activity_geo": "sensitive_geo_string", "hashtag": "sensitive_hashtag_string"}

@mod.route('/')
def ajax_imagine():
    uid = request.args.get('uid', '') # uid
    query_keywords = request.args.get('keywords','') # query dict and corresponding weight
    keywords_list = query_keywords.split(',')
    query_weight = request.args.get('weight','')
    weight_list = query_weight.split(',')

    if len(keywords_list) != len(weight_list):
        return json.dumps([])

    query_fields_dict = {}
    for i in range(len(keywords_list)):
        if shift_dict.has_key(keywords_list[i]):
            keywords_list[i] = shift_dict[str(keywords_list[i])]
        query_fields_dict[keywords_list[i]] = int(weight_list[i])

    field = request.args.get('field', '')
    query_fields_dict['field'] = field

    size = request.args.get('size', 15)
    query_fields_dict['size'] = int(size)
    if uid and query_fields_dict:
        result = imagine(uid, query_fields_dict)
    if result:
        return json.dumps(result)

    return json.dumps([])


