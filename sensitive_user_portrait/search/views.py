# -*- coding:utf-8 -*-

import os
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from sensitive_user_portrait.global_utils import es_sensitive_user_portrait as es
from utils import full_text_search

#mod = Blueprint('search', __name__, url_prefix='/search')

@mod.route('/full_text_search/')
def ajax_full_text_search():
    words_string = request.args.get('words_list', '') #','seperate, 'a,b,c'
    if not words_string:
        return '0'

    words_list = words_string.split(',')
    results = full_text_search(words_list)

    if results:
        return json.dumps(results)
    else:
        return json.dumps([])


