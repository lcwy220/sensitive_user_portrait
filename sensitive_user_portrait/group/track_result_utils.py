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
from sensitive_user_portrait.time_utils import ts2datetime, datetime2ts, ts2date, date2ts
from sensitive_user_portrait.global_utils import es_user_profile

task_index_name = 'group_result'
task_index_type = 'group'

text_index_name = 'monitor_user_text'
text_index_type = 'text'

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
    #start_ts = datetime2ts(task_submit_date)
    start_ts = date2ts(task_submit_date)
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    #test
    now_ts = datetime2ts('2013-09-02')
    date_ts = datetime2ts(now_date)
    segment = int((now_ts - date_ts) / 900) + 1
    end_ts = date_ts + segment * 900
    #every search time-range: 4 hour----bulk action to search
    begin_ts = start_ts

    while True:
        if begin_ts >= end_ts:
            break
        compute_ts = ts2date(begin_ts)
        print 'compute ts:', compute_ts
        query_body = {'range':{'timestamp':{'from': begin_ts, 'to':begin_ts+search_time_segment}}}
        try:
            mid_result_list = es.search(index=monitor_index_name, doc_type=task_name, body={'query':query_body, 'size':100000, 'sort':[{'timestamp':{'order': 'asc'}}]})['hits']['hits']
        except Exception, e:
            raise e
        if mid_result_list:
            for mid_result_item in mid_result_list:
                result_item = mid_result_item['_source']
                timestamp = result_item['timestamp']
                #attr_count
                print 'compute_count'
                count_dict = json.loads(result_item['count'])
                for sensitive in count_dict:
                    count_key = 'count_' + sensitive
                    result[count_key][str(timestamp)] = count_dict[sensitive]
                #attr_sentiment
                print 'compute_sentiment'
                sensitive_sentiment_dict = json.loads(result_item['sentiment'])
                for sensitive in sensitive_sentiment_dict:
                    sentiment_dict = sensitive_sentiment_dict[sensitive]
                    for sentiment in sentiment_dict:
                        sentiment_key = 'sentiment_'+sentiment
                        result[sentiment_key][str(timestamp)] = sentiment_dict[sentiment]
                #attr_sensitive_score
                print 'compute_sensitive_word'
                if 'sensitive_word' in result_item:
                    sensitive_word_dict = json.loads(result_item['sensitive_word'])
                else:
                    sensitive_word_dict = {}
                ts_word_score = 0
                for word in sensitive_word_dict:
                    #print 'word:', json.dumps(word.encode('utf-8')), word.encode('utf-8'), type(word.encode('utf-8'))
                    search_word = word.encode('utf-8')
                    #print 'search_word:', search_word, type(search_word)
                    word_identify = json.loads(word_r.hget('sensitive_words', search_word))
                    ts_word_score += sensitive_word_dict[word] * word_identify[0]
                result['sensitive_score'][str(timestamp)] = ts_word_score
                #attr_geo
                print 'compute geo'
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
                print 'compute hashtag'
                if 'hashtag' in result_item:
                    sensitive_hashtag_dict = json.loads(result_item['hashtag'])
                else:
                    sensitive_hashtag_dict = {}
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

        begin_ts += search_time_segment
    # compute peak for count/sentiment/sensitive_score
    peak_compute_field = ['count_0', 'count_1', 'sentiment_126', 'sentiment_127', 'sentiment_128',\
                          'sentiment_129', 'sentiment_130', 'sensitive_score']
    print 'compute_peak'
    for field in peak_compute_field:
        complement_item = complement_ts(result[field], start_ts, end_ts)
        sort_complement_item = sorted(complement_item.items(), key=lambda x:int(x[0]))
        detect_peaks_input = [item[1] for item in sort_complement_item]
        print 'start_detect_peaks'
        result[field+'_peak'] = detect_peaks(detect_peaks_input)
        result[field] = sort_complement_item
        
    return result

# add ts with value is 0
def complement_ts(result_dict,start_ts, end_ts):
    ts = start_ts
    time_segment = 900
    print 'start_ts:', ts2date(ts)
    print 'end_ts:', ts2date(end_ts)
    print 'result_dict:', result_dict
    while True:
        if ts > end_ts:
            break
        print 'ts:', ts2date(ts)
        if str(ts) not in result_dict:
            result_dict[str(ts)] = 0
        ts += time_segment
    return result_dict


# get monitor user be_comment trend and be_retweet trend from redis
def get_user_comment_retweet(task_exist):
    result = {} # result = {'uid1_comment':{ts:value}, 'uid1_retweet':{ts_value}, 'uid2_comment'}
    submit_date = task_exist['submit_date']
    start_ts = date2ts(submit_date)
    task_status = task_exist['status']
    if task_status == 1:
        now_ts = time.time()
        now_date = ts2datetime(now_ts)
        now_date_ts = datetime2ts(now_date)
        segment = int((now_ts - now_date_ts) / 900) + 1
        end_ts = now_date_ts + segment * 900
        #test
        end_ts = datetime2ts('2013-09-02')
    else:
        end_ts = date2ts(task_exist['end_date'])

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
        # use to detect peaks
        comment_dict = result[user+'_comment']
        complement_comment_dict = complement_ts(comment_dict, start_ts, end_ts)
        sort_comment_dict = sorted(complement_comment_dict.items(), key=lambda x:int(x[0]))
        detect_peaks_comment_input = [item[1] for item in sort_comment_dict]
        result[user+'_comment_peak'] = detect_peaks(detect_peaks_comment_input)

        retweet_dict = result[user+'_retweet']
        complement_retweet_dict = complement_ts(retweet_dict, start_ts, end_ts)
        sort_retweet_dict = sorted(complement_retweet_dict.items(), key=lambda x:int(x[0]))
        detect_peaks_retweet_input = [item[1] for item in sort_retweet_dict]
        result[user+'_retweet_peak'] = detect_peaks(detect_peaks_retweet_input)
        
    return result

# get monitor user social network
def get_network(task_exist):
    result = {}
    return result


# get user information from user_profile
def get_user_info(uid_list):
    result = []
    for uid in uid_list:
        try:
            uid_profile = es_user_profile(index='weibo_user', doc_type='user', id=uid)['_source']
        except:
            uid_profile = {}
        if uid_profile:
            uname = uid_profile['nick_name']
            location = uid_profile['location']
            friendsnum = uid_profile['friendsnum']
            fansnum = uid_profile['fansnum']
            statusnum = uid_profile['statusnum']
        else:
            uname = u'未知'
            location = u'未知'
            friendsnum = u'未知'
            fansnum = u'未知'
            statusnum = u'未知'
        result.append([uid, uname, location, friendsnum, fansnum, statusnum])
    return result


def get_track_result(task_name, module):
    #step1: identify the task_name is in ES(group_result)
    #step2: based on the module to get result
    result = {}
    task_exist = identify_task(task_name)
    if task_exist == None:
        return 'the task is not exist'
    if module=='basic':
        user_info_list = get_user_info(task_exist['uid_list'])
        task_exist['uid_list'] = user_info_list
        result['basic'] = task_exist
        task_submit_date = task_exist['submit_date']
        mid_result = compute_mid_result(task_name, task_submit_date)
        result = dict(result, **mid_result)
    elif module=='comment_retweet':
        result = get_user_comment_retweet(task_exist)
    elif module=='network':
        result = get_network(task_exist)
    else:
        return 'not exist this module: %s' % module
    return result


# based on uid to get uname
def uid2uname(uid):
    try:
        user_item = es_user_profile.get(index=profile_index_name, doc_type=profile_index_type,\
                  id=uid)['_source']
    except:
        user_item = None
    if not user_item:
        return u'未知'
    uname = user_item['nick_name']
    return uname


# show weibo when click count node
def get_count_weibo(task_name, sensitive_status, timestamp):
    result = []
    #step1: get task_user
    #step2: search weibo by conditon: task_user, timestamp, sensitive_status
    task_exist = identify_task(task_name)
    if not task_exist:
        return 'task is not exist'
    task_user = task_exist['uid_list']
    query_body = []
    # multi-search: uid list
    nest_body_list = []
    for uid in task_user:
        nest_body_list.append({'term':{'uid': uid}})
    query_body.append({'bool':{'should':nest_body_list}})
    # range search: timestamp timestamp+900
    query_body.append({'range':{'timestamp':{'from':timestamp, 'to':timestamp+900}}})
    # match search: sensitive_status
    query_body.append({'term':{'sensitive': sensitive_status}})
    try:
        weibo_result = es.search(index=text_index_name, doc_type=text_index_type, \
                body={'query':{'bool':{'must': query_body}}, 'sort':[{'timestamp':{'order':'asc'}}], 'size':10000})['hits']['hits']
    except Exception, e:
        raise e
    for weibo_item in weibo_result:
        weibo_dict = weibo_item['_source']
        uid = weibo_dict['uid']
        uname = uid2uname(uid)
        timestamp = weibo_dict['timestamp']
        date = ts2date(timestamp)
        geo = weibo_dict['geo']
        text = weibo_dict['text']
        result.append([uid, uname, date, geo, text])

    return result

# show weibo when click sentiment node
def get_sentiment_weibo(task_name, sentiment, timestamp):
    result = []
    #step1: get task user
    #step2: search weibo by condition: task_user, sensitive_status, sentiment, timestamp
    task_exist = identify_task(task_name)
    if not task_exist:
        return 'the task is not exist'
    task_user = task_exist['uid_list']
    query_body = []
    # multi-search: uid_list
    nest_body_list = []
    for uid in task_user:
        nest_body_list.append({'term':{'uid': uid}})
    query_body.append({'bool':{'should': nest_body_list}})
    # range search: timestamo timestamp+900
    query_body.append({'range':{'timestamp':{'from': timestamp, 'to':timestamp+900}}})
    # match search: sensitive_status
    #query_body.append({'term': {'sensitive': sensitive_status}})
    # match search: sentiment
    query_body.append({'term': {'sentiment': sentiment}})
    try:
        weibo_result = es.search(index=text_index_name, doc_type=text_index_type, \
                body={'query':{'bool':{'must': query_body}}, 'sort':[{'timestamp': {'order':'asc'}}], 'size':10000})['hits']['hits']
    except Exception, e:
        raise e
    for weibo_item in weibo_result:
        weibo_dict = weibo_item['_source']
        uid = weibo_dict['uid']
        uname = uid2uname(uid)
        text = weibo_dict['text']
        timestamp = weibo_dict['timestamp']
        date = ts2date(timestamp)
        geo = weibo_dict['geo']
        result.append([uid, uname, geo, date, text])

    return result

# show sensitive word when click sensitive word
def get_sensitive_word(task_name, timestamp):
    #step1: get task user
    #step2: get sensitive word from mid-result by condition: task_name, timestamp
    task_exist = identify_task(task_name)
    if not task_exist:
        return 'the task is not exist'
    try:
        task_mid_result = es.get(index=monitor_index_name, doc_type=task_name, id=str(timestamp))['_source']
    except:
        result = None
    sensitive_word_dict = json.loads(task_mid_result['sensitive_word'])
    sort_sensitive_word = sorted(sensitive_word_dict.items(), key=lambda x:x[1], reverse=True)

    return sort_sensitive_word

# show user when click geo
def get_geo_user(task_name, geo, timestamp):
    result = []
    #step1: get task user
    #step2: get user search from monitor_user_text by condition: task_name, timestamp, geo
    task_exist = identify_task(task_name)
    if not task_exist:
        return 'the task is not exist'
    task_user = task_exist['uid_list']
    query_body = []
    # multi-search: task user
    nest_body_list = []
    for user in task_user:
        nest_body_list.append({'term':{'uid': user}})
    query_body.append({'bool':{'should':nest_body_list}})
    # term search: geo
    geo_list = geo.split('\t')
    city = geo_list[-1]
    query_body.append({'wildcard':{'geo': '*' + city + '*'}})
    # range search: timestamp timestamp+900
    query_body.append({'range':{'timestamp':{'from': timestamp, 'to':timestamp+3600*24}}})
    try:
        weibo_dict_result = es.search(index=text_index_name, doc_type=text_index_type, \
                body={'query':{'bool':{'must': query_body}}, 'size':10000})['hits']['hits']
    except Exception, e:
        raise e
    uid_dict = {}
    for weibo_dict in weibo_dict_result:
        weibo_item = weibo_dict['_source']
        uid = weibo_item['uid']
        try:
            uid_dict[uid] += 1
        except:
            uid_dict[uid] = 1
    sort_uid_dict = sorted(uid_dict.items(), key=lambda x:x[1], reverse=True)
    for uid_item in sort_uid_dict:
        uid = uid_item[0]
        uname = uid2uname(uid)
        count = uid_item[1]
        result.append([uid, uname, count])
    return result

# show weibo when click geo
def get_geo_weibo(task_name, geo, timestamp):
    result = []
    #step1: identify task exist
    #step2: search weibo from monitor_user_text by condition:task_user, geo, timestamp
    task_exist = identify_task(task_name)
    if not task_exist:
        return 'the task is not exist'
    task_user = task_exist['uid_list']
    query_body = []
    # multi-search: task user
    nest_body_list = []
    for uid in task_user:
        nest_body_list.append({'term':{'uid': uid}})
    query_body.append({'bool':{'should': nest_body_list}})
    # range-search: task user
    query_body.append({'range':{'timestamp':{'from': timestamp, 'to': timestamp+24*3600}}})
    # term-search: geo
    geo_list = geo.split('\t')
    city = geo_list[-1]
    query_body.append({'wildcard': {'geo': '*' + city + '*'}})
    try:
        weibo_dict_list = es.search(index=text_index_name, doc_type=text_index_type, \
                body={'query':{'bool':{'must': query_body}}, 'sort':[{'timestamp':{'order': 'asc'}}], 'size':10000})['hits']['hits']
    except Exception, e:
        raise e
    for weibo_dict in weibo_dict_list:
        weibo_item  = weibo_dict['_source']
        uid = weibo_item['uid']
        uname = uid2uname(uid)
        text = weibo_item['text']
        timestamp = weibo_item['timestamp']
        date = ts2date(timestamp)
        geo = weibo_item['geo']
        result.append([uid, uname, geo, date, text])
    return result

