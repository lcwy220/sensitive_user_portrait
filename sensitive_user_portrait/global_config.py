# -*- coding: utf-8 -*-

import os
from flask import Flask

REDIS_CLUSTER_HOST_FLOW1 = '219.224.135.93'
REDIS_CLUSTER_HOST_FLOW1_LIST = ["219.224.135.91", "219.224.135.92", "219.224.135.93"]
REDIS_CLUSTER_PORT_FLOW1 = '7379'
REDIS_CLUSTER_PORT_FLOW1_LIST = ["7379", "7380"]
REDIS_CLUSTER_HOST_FLOW2 = '219.224.135.94'
REDIS_CLUSTER_PORT_FLOW2 = '7379'
REDIS_HOST = '219.224.135.97'
REDIS_PORT = '7380'

USER_ES_HOST = '219.224.135.97'
ES_CLUSTER_HOST_FLOW1 = ["219.224.135.93:9206","219.224.135.94:9206"]

ZMQ_VENT_PORT_FLOW1 = '7387'
ZMQ_CTRL_VENT_PORT_FLOW1 = '6585'
ZMQ_VENT_HOST_FLOW1 = '219.224.135.93'
ZMQ_CTRL_HOST_FLOW1 = '219.224.135.93'

ZMQ_VENT_PORT_FLOW2 = '7388'
ZMQ_CTRL_VENT_PORT_FLOW2 = '6586'

ZMQ_VENT_PORT_FLOW3 = '7389'
ZMQ_CTRL_VENT_PORT_FLOW3 = '6587'

ZMQ_VENT_PORT_FLOW4 = '7390'
ZMQ_CTRL_VENT_PORT_FLOW4 = '6588'

ZMQ_VENT_PORT_FLOW5 = '7391'
ZMQ_CTRL_VENT_PORT_FLOW5 = '6589'

# csv file path
'''
BIN_FILE_PATH = '/home/ubuntu8/yuankun/data' # '219.224.135.93:/home/ubuntu8/yuankun'
'''
BIN_FILE_PATH = '/home/ubuntu8/data1309/20130901'

# first part of csv file
FIRST_FILE_PART = 'MB_QL_9_3_NODE'

# sensitive words path
SENSITIVE_WORDS_PATH = '/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/flow4/sensitive_words.txt'

# need three ES identification 
USER_PROFILE_ES_HOST = ['219.224.135.96:9208','219.224.135.97:9208','219.224.135.98:9208']
USER_PROFILE_ES_PORT = 9208
SENSITIVE_USER_PORTRAIT_ES_HOST = '219.224.135.93:9206'
SENSITIVE_USER_PORTRAIT_ES_PORT = '9206'

# use to identify the db number of redis-97
R_BEGIN_TIME = '2013-09-01'

# use to recommentation
RECOMMENTATION_FILE_PATH = '/home/ubuntu8/huxiaoqian/user_portrait/recommentaion_file'
RECOMMENTATION_TOPK = 10000

# use to config leveldb
DEFAULT_LEVELDBPATH = '/home/ubuntu8/huxiaoqian/user_portrait_leveldb'

# use to upload the user list for group task
UPLOAD_FOLDER = '/home/ubuntu8/huxiaoqian/user_portrait/cron/group/upload/'
ALLOWED_EXTENSIONS = set(['txt'])

"""
# use to save user_portrait weibo 7day
XAPIAN_DB_PATH = 'user_portrait_weibo'
XAPIAN_DATA_DIR = '/home/ubuntu8/huxiaoqian/user_portrait_weibo_xapian/data/'
XAPIAN_STUB_FILE_DIR = '/home/ubuntu8/huxiaoqian/user_portrait_weibo_xapian/stub/'

XAPIAN_INDEX_SCHEMA_VERSION = 5
XAPIAN_INDEX_LOCK_FILE = '/tmp/user_portrait_weibo_xapian'

XAPIAN_SEARCH_DEFAULT_SCHEMA_VERSION = 5

XAPIAN_ZMQ_POLL_TIMEOUT = 100000
"""

# all weibo database
WEIBO_API_HOST = ''
WEIBO_API_PORT = ''

