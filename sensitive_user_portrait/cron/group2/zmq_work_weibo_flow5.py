# -*- coding=utf-8 -*-

import IP
import re
import csv
import sys
import zmq
import time
import json
import math
from datetime import datetime
from DFA_filter import readInputText, createWordTree, searchWord

reload(sys)
sys.path.append('../../')
from time_utils import ts2datetime, datetime2ts
from global_config import ZMQ_VENT_PORT_FLOW5, ZMQ_CTRL_VENT_PORT_FLOW5,\
                          ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_HOST_FLOW1
from global_utils import R_GROUP as r
from global_utils import MONITOR_REDIS as monitor_r

# use to get track user by hour
def get_track_task_user():
    user_list = []
    user_list = r.hkeys('track_task_user')
    return user_list


# add 1 to monitor user comment count
def add_comment(item):
    root_uid = item['root_uid']
    timestamp = item['timestamp']
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    time_segment = int((timestamp - date_ts) / 900)
    start_ts = date_ts + time_segment * 900
    key = 'comment_' + str(start_ts)
    monitor_r.hincrby(str(root_uid), key, 1)
    

# add 1 to monitor user retweet count
def add_retweet(item):
    root_uid = item['root_uid']
    timestamp = item['timestamp']
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    time_segment = int((timestamp - date_ts) / 900)
    start_ts = date_ts + time_segment * 900
    key = 'retweet_' + str(start_ts)
    monitor_r.hincrby(str(root_uid), key, 1)


if __name__ == "__main__":
    """
     receive weibo
    """
    context = zmq.Context()

    receiver = context.socket(zmq.PULL)
    receiver.connect('tcp://%s:%s' %(ZMQ_VENT_HOST_FLOW1, ZMQ_VENT_PORT_FLOW5))

    controller = context.socket(zmq.SUB)
    controller.connect("tcp://%s:%s" %(ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_VENT_PORT_FLOW5))

    count = 0
    read_count = 0
    tb = time.time()
    ts = tb
    sensitive_words = createWordTree()
    monitor_user_list = get_track_task_user()
    print 'monitor_user_list:', monitor_user_list
    update_user_ts = time.time()
    bulk_action = []
    while 1:
        '''
        use to update user list by 15min
        '''
        update_user_te = time.time()
        if (update_user_te - update_user_ts) % 900 == 0:
            print 'update track user list'
            monitor_user_list = get_track_task_user()

        item = receiver.recv_json()
        if not item:
            continue 
        
        if item['sp_type'] == '1':
            read_count += 1
            #print 'item:', item
            if str(item['root_uid']) in monitor_user_list:
                if item['message_type'] != 2:
                    add_comment(item)
                elif item['message_type'] != 3:
                    add_retweet(item)

        if read_count % 10000 == 0:
            te = time.time()
            print '[%s] cal speed: %s sec/per %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), te - ts, 10000) 
            if read_count % 100000 == 0:
                print '[%s] total cal %s, cost %s sec [avg %s per/sec]' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), read_count, te - tb, read_count / (te - tb)) 
            ts = te
