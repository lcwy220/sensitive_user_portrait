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
from global_config import ZMQ_VENT_PORT_FLOW4, ZMQ_CTRL_VENT_PORT_FLOW4,\
                          ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_HOST_FLOW1
from global_utils import es_sensitive_user_portrait as es
from global_utils import R_GROUP as r

reload(sys)
sys.path.append('../../../../../libsvm-3.17/python/')
from sta_ad import load_scws

sw = load_scws()
cx_dict = ['a', 'n', 'nr', 'ns', 'nz', 'v', '@', 'd']

index_name = 'monitor_user_text'
index_type = 'text'


# get sentiment dict
def get_liwc_dict():
    results = dict()
    f = open('/home/ubuntu8/huxiaoqian/sensitive_user_portrait/sensitive_user_portrait/cron/group/extract_word.csv', 'rb')
    reader = csv.reader(f)
    for line in reader:
        num = line[0]
        word = line[1]
        try:
            results[num].add(word)
        except:
            results[num] = set([word])
    return results

liwc_dict = get_liwc_dict()


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
    index_body['uid'] = str(item['uid'])
    index_body['text'] = item['text']
    index_body['mid'] = str(item['mid'])
    index_body['sensitive'] = item['sensitive']
    index_body['sentiment'] = item['sentiment']
    index_body['timestamp'] = int(item['timestamp'])
    index_body['message_type'] = item['message_type']
    if item['message_type'] != 1:
        index_body['root_mid'] = str(item['root_mid'])
        index_body['root_uid'] = str(item['root_uid'])
    ip = item['send_ip']
    index_body['ip'] = ip
    index_body['geo'] = ip2city(ip)
    try:
        index_body['hashtag'] = item['hashtag']
    except:
        pass
    try:
        index_body['sensitive_word'] = item['sensitive_word']
    except:
        pass
    action = {'index': {'_id': index_body['mid']}}
    xdata = index_body
    return action, xdata


# use to get track user by hour
def get_track_task_user():
    user_list = []
    user_list = r.hkeys('track_task_user')
    return user_list

# use to identify the sentiment
def get_sentiment_attribute(text):
    results = {}
    cut_text = sw.participle(text.encode('utf-8'))
    cut_word_set = set([term for term, cx in cut_text if cx in cx_dict])
    max_count = 0
    max_sentiment = 0
    for num in liwc_dict:
        liwc_word_set = liwc_dict[num]
        union_count = len(cut_word_set & liwc_word_set)
        if union_count > max_count:
            max_count = union_count
            max_sentiment = num
    #print 'max_sentiment:', max_sentiment
    #print 'max_count:', max_count
    if max_sentiment == 0:
        max_sentiment = '130' # mark: sentiment is other
    return max_sentiment

def get_hashtag_attribute(text):
    hashtag_string = ''
    user_text_list = text.split('//@')
    if user_text_list:
        user_text = user_text_list[0]
    else:
        user_text = text
    if len(user_text) != 0:
        if isinstance(user_text, str):
            user_text = user_text.decode('utf-8', 'ignore')
            RE = re.compile(u'#([a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+)#', re.UNICODE)
            hashtag_list = RE.findall(user_text)
            if hashtag_list:
                hashtag_string = '&'.join(hashtag_list)

    return hashtag_string


if __name__ == "__main__":
    """
     receive weibo
    """
    context = zmq.Context()

    receiver = context.socket(zmq.PULL)
    receiver.connect('tcp://%s:%s' %(ZMQ_VENT_HOST_FLOW1, ZMQ_VENT_PORT_FLOW4))

    controller = context.socket(zmq.SUB)
    controller.connect("tcp://%s:%s" %(ZMQ_VENT_HOST_FLOW1, ZMQ_CTRL_VENT_PORT_FLOW4))

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
            if str(item['uid']) in monitor_user_list:
                text = item['text']
                # add sensitive field and sensitive_word field to weibo
                sw_list = searchWord(text.encode('utf-8'))
                sensitive = len(sw_list)
                if sensitive:
                    item['sensitive'] = 1
                    word_set = set()
                    for w in sw_list:
                        word = ''.join([chr(x) for x in w])
                        word = word.decode('utf-8')
                        word_set.add(word)
                    sensitive_word_string = '&'.join(list(word_set))
                    item['sensitive_word'] = sensitive_word_string
                else:
                    item['sensitive'] = 0
                # add sentiment field to weibo
                sentiment = get_sentiment_attribute(text)
                item['sentiment'] = sentiment
                # add hashtag field to weibo
                hashtag_string = get_hashtag_attribute(text)
                if hashtag_string != '':
                    item['hashtag'] = hashtag_string
                # save
                action, xdata = expand_index_action(item)
                bulk_action.extend([action, xdata])
                count += 1
        
        if count % 1 == 0 and count != 0:
            print 'start bulk_action %s' % count
            es.bulk(bulk_action, index=index_name, doc_type=index_type, timeout=60)
            bulk_action = []
            count = 0
        
        if read_count % 10000 == 0:
            te = time.time()
            print '[%s] cal speed: %s sec/per %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), te - ts, 10000) 
            if read_count % 100000 == 0:
                print '[%s] total cal %s, cost %s sec [avg %s per/sec]' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), read_count, te - tb, read_count / (te - tb)) 
            ts = te
