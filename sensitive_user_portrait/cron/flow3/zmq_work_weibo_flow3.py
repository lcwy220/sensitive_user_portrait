# -*- coding=utf-8 -*-

import re
import sys
import zmq
import time
import json
import math
from datetime import datetime
from test_save_attribute import save_ruid
from DFA_filter import readInputText, createWordTree, searchWord

reload(sys)
sys.path.append('../../')
from time_utils import ts2datetime, datetime2ts
from global_config import ZMQ_VENT_PORT_FLOW3, ZMQ_CTRL_VENT_PORT_FLOW3,\
                          ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_HOST_FLOW1
from global_utils import R_CLUSTER_FLOW2 as r_cluster

def extract_uname(text):
    at_uname_list = []
    if isinstance(text, str):
        text = text.decode('utf-8', 'ignore')
    text = text.split('//@')[0]
    RE = re.compile(u'@([a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+) ', re.UNICODE)
    repost_chains = RE.findall(text)

    return repost_chains

def cal_propage_work(item, sensitive):
    uid = item['uid']
    timestamp = item['timestamp']

    #r_uid = item['retweeted_uid']
    r_uid = item['root_uid']
    save_ruid(uid, r_uid, timestamp, sensitive)

def cal_hashtag_work(item, sensitive):
    text = item['text']
    uid = item['uid']
    timestamp = item['timestamp']
    ts = ts2datetime(timestamp).replace('-','')

    if isinstance(text, str):
        text = text.decode('utf-8', 'ignore')
    RE = re.compile(u'#([a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+)#', re.UNICODE)
    hashtag_list = RE.findall(text)
    if hashtag_list:
        hashtag_dict = {}
        for hashtag in hashtag_list:
            try:
                hashtag_dict[hashtag] += 1
            except:
                hashtag_dict[hashtag] = 1

        try:
            if sensitive:
                hashtag_count_string = r_cluster.hget('sensitive_hashtag_'+str(ts), str(uid))
            else:
                hashtag_count_string = r_cluster.hget('hashtag_'+str(ts), str(uid))
            hashtag_count_dict = json.loads(hashtag_count_string)
            for hashtag in hashtag_dict:
                count = hashtag_dict[hashtag]
                try:
                    hashtag_count_dict[hashtag] += count
                except:
                    hashtag_count_dict[hashtag] = count
            if sensitive:
                r_cluster.hset('sensitive_hashtag_'+str(ts), str(uid), json.dumps(hashtag_count_dict))
            else:
                r_cluster.hset('hashtag_'+str(ts), str(uid), json.dumps(hashtag_count_dict))
        except:
            if sensitive:
                r_cluster.hset('sensitive_hashtag_'+str(ts), str(uid), json.dumps(hashtag_dict))
            else:
                r_cluster.hset('hashtag_'+str(ts), str(uid), json.dumps(hashtag_dict))

def cal_sensitive_words_work(item, sw_list):
    timestamp = ts2datetime(timestamp).replace('-','')
    map = {}
    for w in sw_list:
        word = "".join([chr(x) for x in w])
        word = word.decode('utf-8')
        if not map.__contains__(word):
            map[word] = 1
        else:
            map[word] += 1
    try:
        sensitive_count_string = r_cluster.hget('sensitive_'+str(ts), str(uid))
        sensitive_count_dict = json.loads(sensitive_count_string)
        for word in map:
            count = map[word]
            if sensitive_count_dict.__contains__(word):
                sensitive_count_dict[word] += count
            else:
                sensitive_count_dict[word] = count
        r_cluster.hset('sensitive_'+str(ts), str(uid), json.dumps(sensitive_count_dict))
    except:
        r_cluster.hset('sensitive_'+str(ts), str(uid), json.dumps(map))

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
    while 1:
        item = receiver.recv_json()
        if not item:
            continue 


        if item['sp_type'] == '1':
            text = item['text']
            sw_list = searchWord(text.encode('utf-8'))
            sensitive = len(sw_list)
            cal_hashtag_work(item, sensitive) # hashtag 
            if item and item['message_type']==3:
                cal_propage_work(item, sensitive) # retweet relationship
            if sensitive:
                cal_sensitive_words_work(item, sw_list) # sensitive_words
            count += 1

        if count % 10000 == 0:
            te = time.time()
            print '[%s] cal speed: %s sec/per %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), te - ts, 10000) 
            if count % 100000 == 0:
                print '[%s] total cal %s, cost %s sec [avg %s per/sec]' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), count, te - tb, count / (te - tb)) 
            ts = te
