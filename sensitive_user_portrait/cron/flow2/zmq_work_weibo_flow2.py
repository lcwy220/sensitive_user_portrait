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
from test_save_attribute import save_at, cal_hashtag_work

reload(sys)
sys.path.append('../../')
from time_utils import ts2datetime, datetime2ts
from global_config import ZMQ_VENT_PORT_FLOW2, ZMQ_CTRL_VENT_PORT_FLOW2,\
                          ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_HOST_FLOW1
from global_utils import es_flow_text as es_text
from global_utils import R_RECOMMENTATION as r
from DFA_filter import createWordTree, searchWord
Fifteenminutes = 900

def extract_uname(text):
    at_uname_list = []
    if isinstance(text, str):
        text = text.decode('utf-8', 'ignore')
    text = text.split('//@')[0]
    RE = re.compile(u'@([a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+) ', re.UNICODE)
    repost_chains = RE.findall(text)

    return repost_chains

def extract_hashtag(text):
    if isinstance(text, str):
        text = text.decode('utf-8', 'ignore')
    RE = re.compile(u'#([a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+)#', re.UNICODE)
    hashtag_list = RE.findall(text)

    return hashtag_list

def cal_propage_work(item):
    uid = item['uid']
    timestamp = item['timestamp']
    text = item['text']
    sensitive_words_dict = searchWord(text.encode('utf-8', 'ignore'), DFA)
    sensitive = len(sensitive_words_dict)

    #if sensitive:
    #    r.sadd('sensitive_user', uid) # 敏感微博用户集合

    #ip = item['geo']
    ip = item['send_ip']
    # attribute location
    if ip:
        save_city(uid, ip, timestamp, sensitive)

    # attribute activity
    date = ts2datetime(timestamp)
    ts = datetime2ts(date)
    time_segment = (timestamp - ts) / Fifteenminutes
    save_activity(uid, timestamp, time_segment, sensitive)

    # attribute mention
    at_uname_list = extract_uname(text)
    try:
        if at_uname_list:
            at_uname = at_uname_list[0]
            if at_uname != '':
                save_at(uid, at_uname, timestamp, sensitive)
    except:
        pass

    # hashtag
    hashtag_list = extract_hashtag(text)
    if hashtag_list:
        cal_hashtag_work(uid, hashtag_list, timestamp, sensitive)


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
    DFA = createWordTree()


    while 1:
        item = receiver.recv_json()

        if not item:
            continue 

        if int(item['sp_type']) == 1:
            cal_propage_work(item)
            count += 1

            if count % 10000 == 0:
                te = time.time()
                print '[%s] cal speed: %s sec/per %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), te - ts, 10000) 
                if count % 100000 == 0:
                    print '[%s] total cal %s, cost %s sec [avg %s per/sec]' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), count, te - tb, count / (te - tb)) 
                ts = te
                if count % 1000000 == 0:
                    DFA = createWordTree()
