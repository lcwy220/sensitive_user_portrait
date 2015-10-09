# -*- coding: UTF-8 -*-
'''
use to get track result by module
'''
import sys
import time
import json
from peak_detection import detect_peaks
from sensitive_user_portrait.global_utils import es_sensitive_user_portrait as es
from sensitive_user_portrait.global_utils import MONITOR_REDIS as monitor_r
from sensitive_user_portrait.global_utils import R_RECOMMENTATION as word_r

task_index_name = 'group_result'
task_index_type = 'group'

monitor_index_name = 'monitor_result'
#monitor_index_type: task_name

# identify the task_name exist and get basic result
def identify_task(task_name):
    try:
        task_exist = es.get(index=task_index_name, doc_type=task_index_type, id=task_name)['_source']
    except:
        task_exist = None

    return task_exist

def compute_mid_result(task_name, task_submit_date):
    result = {'count_0':{}, 'count_1':{}, 'sentiment_126':{}, 'sentiment_127':{}, 'sentiment_128':{},\
            'sentiment_129':{}, 'sentiment_130':{}, 'sensitive_score':{}, 'geo_0':{}, 'geo_1':{},\
            'hashtag_0':{}, 'hashtag_1':{}}
    #geo & hashtag: day
    #other: 15min
    search_time_segment = 3600 * 4
    start_ts = datetime2ts(task_submit_date)
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    date_ts = datetime2ts(now_date)
    segment = int((now_ts - date_ts) / 900) + 1
    end_ts = date_ts + segment * 900
    #every search time-range: 4 hour----bulk action to search
    begin_ts = start_ts

    while True:
        if begin_ts >= end_ts:
            break
        query_body = {'range':{'timestamp':{'from': begin_ts, 'to':beigin_ts+search_time_segment}}}
        try:
            mid_result_list = es.search(index=monitor_index_name, doc_type=task_name, body={'query':query_body, 'size':100000, 'sort':[{'timestamp':{'order': 'asc'}}]})['hits']['hits']
        except Exception, e:
            raise e
        if mid_result_list:
            for mid_result_item in mie_result_list:
                result_item = mid_result_item['_source']
                timestamp = result_item['timestamp']
                #attr_count
                count_dict = json.loads(result_item['count'])
                for sensitive in count_dict:
                    count_key = 'count_' + sensitive
                    result[count_key][str(timestamp)] = count_dict[sensitive]
                #attr_sentiment
                sentiment_dict = json.loads(result_item['sentiment'])
                for sentiment in sentiment_dict:
                    sentiment_key = 'sentiment_'+sentiment
                    result[sentiment_key][str(timestamp)] = sentiment_dict[sentiment]
                #attr_sensitive_score
                sensitive_word_dict = json.loads(result_item['sensitive_word'])
                ts_word_score = 0
                for word in sensitive_word_dict:
                    word_identify = json.loads(word_r.hget('sensitive_word', str(word)))
                    ts_word_score += sensitive_word_dict[word] * word_identify[0]
                result['sensitive_score'][str(timestamp)] = ts_word_score
                #attr_geo
                timestamp_date = ts2datetime(timestamp)
                sensitive_geo_dict = json.loads(result_item['geo'])
                for sensitive in sensitive_geo_dict:
                    if timestamp_date not in result['geo_'+sensitive]:
                        result['geo_'+sensitive][timestamp_date] = {}
                    geo_dict = sensitive_geo_dict[sensitive]
                    for geo in geo_dict:
                        try:
                            result['geo_'+sensitive][timestamp_date][geo] += geo_dict[geo]
                        except:
                            result['geo_'+sensitive][timestamp_date][geo] = geo_dict[geo]
                #attr_hashtag
                sensitive_hashtag_dict = json.loads(result_item['hashtag'])
                for sensitive in sensitive_hashtag_dict:
                    for sensitive in sensitive_hashtag_dict:
                        if timestamp_date not in result['hashtag_'+sensitive]:
                            result['hashtag_'+sensitive][timestamp_date] = {}
                        hashtag_dict = sensitive_hashtag_dict[sensitive]
                        for hashtag in hashtag_dict:
                            try:
                                result['hashtag_'+sensitive][timestamp_date][hashtag] += hashtag_dict[hashtag]
                            except:
                                result['hashtag_'+sensitive][timestamp_date][hashtag] = hashtag_dict[hashtag]

        beigin_ts += search_time_segment
    # compute peak for count/sentiment/sensitive_score
    peak_compute_field = ['count_0', 'count_1', 'sentiment_126', 'sentiment_127', 'sentiment_128',\
                          'sentiment_129', 'sentiment_130', 'sensitive_score']
    for field in peak_compute_field:
        complement_item = complement_ts(result[field])
        result[field+'_peak'] = detect_peaks(complement_item)
        result[field] = complement_item
        
    return result

# add ts with value is 0
def complement_ts(result_dict):
    complement_result = {}
    return complement_result


# get monitor user be_comment trend and be_retweet trend from redis
def get_user_comment_retweet(task_exist):
    result = {} # result = {'uid1_comment':{ts:value}, 'uid1_retweet':{ts_value}, 'uid2_comment'}
    task_user = task_exist['uid_list']
    for user in task_user:
        result[user+'_comment'] = {}
        result[user+'_retweet'] = {}
        comment_retweet_dict = monitor_r.hgetall(user)
        for item in comment_retweet_dict:
            item_type_ts = item.split('_')
            item_type = item_type_ts[0]
            item_ts = item_type_ts[1]
            result[user+'_'+item_type][item_ts] = comment_retweet_dict[item]

    return result

# get monitor user social network
def get_network(task_exist):
    result = {}
    return result

def get_track_result(task_name, module):
    #step1: identify the task_name is in ES(group_result)
    #step2: based on the module to get result

    task_exist = identify_task(task_name)
    if task_exist == None:
        return 'the task is not exist'
    if module=='basic':
        result['basic'] = task_exist
        task_submit_date = task_exist['submit_date']
        mid_result = comput_mid_result(task_name, task_submit_date)
        result = dict(result, **mid_result)
    elif module=='comment_retweet':
        result = get_user_comment_retweet(task_exist)
    elif module=='network':
        result = get_network(task_exist)
    else:
        return 'not exist this module: %s' % module
    return result


