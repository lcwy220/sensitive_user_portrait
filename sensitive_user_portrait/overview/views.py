# -*- coding:utf-8 -*-

import os
import time
import sys
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from sensitive_user_portrait.time_utils import datetime2ts, ts2datetime
from sensitive_user_portrait.global_utils import R_RECOMMENTATION as r

mod = Blueprint('overview', __name__, url_prefix='/overview')

@mod.route('/show/')
def ajax_show_all():
    results = r.get('overview')
    if results:
        return results
    else:
        return None



