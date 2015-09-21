#-*- coding:utf-8 -*-

import json
import time
import datetime
from sensitive_user_portrait.time_utils import ts2datetime, ts2date
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect, make_response


mod = Blueprint('', __name__, url_prefix='/index')


@mod.route('/')
def loading():

    return render_template('index.html')

@mod.route('/overview/')
def overview():
    return render_template('overview/html')




