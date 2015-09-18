# -*- coding:utf-8 -*-

import json
import time
import datetime
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect, make_response

mod = Blueprint('portrait', __name__, url_prefix='/index')

@mod.route('/')
def loading():
    return render_template('index.html')
