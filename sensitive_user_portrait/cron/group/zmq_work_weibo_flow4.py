# -*- coding=utf-8 -*-

import IP
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
from global_config import ZMQ_VENT_PORT_FLOW4, ZMQ_CTRL_VENT_PORT_FLOW4,\
                          ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_HOST_FLOW1
from global_utils import es_sensitive_user_portrait as es
from global_utils import G_GROUP as r

index_name = 'monitor_user_text'
index_type = 'text'

# transfer ip to city
def ip2city(ip):
    try:
        city = IP.find(str(ip))
        if city:
            city = city.encode('utf-8')
        else:
            return None
    except Exception, e:
        return None
    return city

# use to expand index body to bulk action
def expand_index_action(item):
    index_body = {}
    index_body['uid'] = item['user']
    index_body['text'] = item['text']
    index_body['mid'] = item['_id']
    index_body['sensitive'] = item['sensitive']
    index_body['timestamp'] = int(item['timestamp'])
    ip = item['geo']
    index_body['ip'] = ip
    index_body['geo'] = ip2city(ip)
    action = {'index': {'_id': index_body['mid']}}
    xdata = {'doc': index_body}
    return action, xdata


# use to get track user by hour
def get_track_task_user():
    user_list = []
    user_list = r.hkeys('track_task_user')
    return user_list


if __name__ == "__main__":
    """
     receive weibo
    """
    context = zmq.Context()

    receiver = context.socket(zmq.PULL)
    receiver.connect('tcp://%s:%s' %(ZMQ_VENT_HOST_FLOW1, ZMQ_VENT_PORT_FLOW3))

    controller = context.socket(zmq.SUB)
    controller.connect("tcp://%s:%s" %(ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_VENT_PORT_FLOW3))

    count = 0
    tb = time.time()
    ts = tb
    sensitive_words = createWordTree()
    monitor_user_list = get_track_task_user()
    update_user_ts = time.time()
    bulk_action = []
    while 1:
        '''
        use to update user list by 15min
        '''
        update_user_te = time.time()
        if (update_user_te - update_user_ts) % 900 == 0:
            monitor_user_list = get_track_utask_user()

        item = receiver.recv_json()
        if not item:
            continue 
        
        
        if item['sp_type'] == '1':
            if item['user'] in monitor_user_list:
                text = item['text']
                sw_list = searchWord(text.encode('utf-8'))
                sensitive = len(sw_list)
                if sensitive:
                    item['sentiment'] = 1
                else:
                    item['sentiment'] = 0
                action, xdata = expand_index_action(info)
                bulk_action.extend([action, xdata])
                count += 1
        if count % 10 == 0:
            es.bulk(bulk_action, index=index_name, doc_type=index_type, timeout=60)
            bulk_action = []
        if count % 10000 == 0:
            te = time.time()
            print '[%s] cal speed: %s sec/per %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), te - ts, 10000) 
            if count % 100000 == 0:
                print '[%s] total cal %s, cost %s sec [avg %s per/sec]' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), count, te - tb, count / (te - tb)) 
            ts = te
