# -*- coding=utf-8 -*-
# personal attribute calculate, include ip, time segment and @

import re
import sys
import zmq
import time
import json
import redis
import math
from datetime import datetime
from test_save_attribute import save_city
from test_save_attribute import save_activity
from test_save_attribute import save_at
from DFA_filter import sensitive_words_extract, createWordTree, searchWord
from elasticsearch import Elasticsearch
from weibo_text_mappings import mappings

reload(sys)
sys.path.append('../../')
from time_utils import ts2datetime, datetime2ts
from global_config import ZMQ_VENT_PORT_FLOW2, ZMQ_CTRL_VENT_PORT_FLOW2,\
                          ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_HOST_FLOW1
from global_utils import es_sensitive_user_text as es_text
from global_utils import R_RECOMMENTATION as r
Fifteenminutes = 900

def extract_uname(text):
    at_uname_list = []
    if isinstance(text, str):
        text = text.decode('utf-8', 'ignore')
    text = text.split('//@')[0]
    RE = re.compile(u'@([a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+) ', re.UNICODE)
    repost_chains = RE.findall(text)

    return repost_chains

def cal_propage_work(item):
    uid = item['uid']
    timestamp = item['timestamp']
    text = item['text']
    sw_list = sensitive_words_extract(text.encode('utf-8'))
    sensitive = len(sw_list)

    if sensitive:
        r.sadd('sensitive_user', uid) # 敏感微博用户集合

    #ip = item['geo']
    ip = item['send_ip']
    # attribute location
    if ip:
        save_city(uid, ip, timestamp, sensitive)

    # attribute activity
    date = ts2datetime(timestamp)
    ts = datetime2ts(date)
    date = date.replace('-','')
    time_segment = (timestamp - ts) / Fifteenminutes
    save_activity(uid, date, time_segment, sensitive)

    # attribute mention
    at_uname_list = extract_uname(text)
    try:
        at_uname = at_uname_list[0]
        save_at(uid, at_uname, timestamp, sensitive)
    except:
        pass



if __name__ == "__main__":

    """
     receive weibo
    """
    context = zmq.Context()

    receiver = context.socket(zmq.PULL)
    receiver.connect('tcp://%s:%s' %(ZMQ_VENT_HOST_FLOW1, ZMQ_VENT_PORT_FLOW2))

    controller = context.socket(zmq.SUB)
    controller.connect("tcp://%s:%s" %(ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_VENT_PORT_FLOW2))

    count = 0
    tb = time.time()
    ts = tb
    bulk_action = []
    #sensitive_words = createWordTree()
    weibo_user = redis.StrictRedis("219.224.135.91", port="7381")

    date = ts2datetime(time.time())
    index_name = date.replace('-', '') + '_weibo'
    index_bool = es_text.indices.exists(index=index_name)
    if not index_bool:
        mappings(es_text, index_name)


    key_list = ['uid', 'mid', 'ip', 'timestamp', 'message_type','root_uid', 'root_mid', 'text']
    send_list = ['uid', 'mid', 'send_ip', 'timestamp', 'message_type', 'root_uid', 'root_mid', 'text']
    while 1:
        item = receiver.recv_json()

        if not item:
            continue 

        if int(item['sp_type']) != 1:
            continue
        item_dict = dict()
        text = item['text']
        direct_uname = extract_uname(text)
        if direct_uname:
            item_dict['direct_uname'] = direct_uname
            direct_uid = weibo_user.hget("weibo_user", direct_uname)
        else:
            item_dict['direct_uname'] = ''
            item_dict['direct_uid'] = item['root_uid']
        #cal_propage_work(item)
        for i in range(len(key_list)):
            item_dict[key_list[i]] = item[send_list[i]]
        if direct_uname and direct_uid:
            item_dict['direct_uid'] = direct_uid
        _id = item['uid']
        action = {'index': {'_id': _id}}
        bulk_action.extend([action, item_dict])
        count += 1
        if count % 1000 == 0:
            if bulk_action:
                es_text.bulk(bulk_action, index=index_name, doc_type='text', timeout=30)
                bulk_action = []
                print count
        if count % 10000 == 0:
            te = time.time()
            print '[%s] cal speed: %s sec/per %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), te - ts, 10000) 
            if count % 100000 == 0:
                print '[%s] total cal %s, cost %s sec [avg %s per/sec]' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), count, te - tb, count / (te - tb)) 
            ts = te
