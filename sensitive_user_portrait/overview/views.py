# -*- coding:utf-8 -*-

import os
import time
import sys
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from sensitive_user_portrait.time_utils import datetime2ts, ts2datetime
from utils import get_attr
mod = Blueprint('overview', __name__, url_prefix='/overview')

@mod.route('/show/')
def ajax_show_all():
    date = request.args.get('date', '') # '2013-09-01'
    date = date.replace('-', '')
    results = get_attr(date)
    if results:
        return json.dumps(results)
    else:
        return None



