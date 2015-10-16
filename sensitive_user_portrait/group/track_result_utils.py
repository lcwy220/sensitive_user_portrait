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
from sensitive_user_portrait.global_utils import MONITOR_INNER_REDIS as monitor_inner_r
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
    result = {'count_0':{}, 'count_1':{}, 'sentiment_0_126':{}, 'sentiment_0_127':{}, 'sentiment_0_128':{},\
            'sentiment_0_129':{}, 'sentiment_0_130':{}, 'sensitive_score':{}, 'geo_0':{}, 'geo_1':{},\
            'hashtag_0':{}, 'hashtag_1':{}, 'sentiment_1_126':{}, 'sentiment_1_127':{}, \
            'sentiment_1_128':{}, 'sentiment_1_129':{}, 'sentiment_1_130':{}}
    #geo & hashtag: day
    #other: 15min
    search_time_segment = 3600 * 4
    #start_ts = datetime2ts(task_submit_date)
    start_ts = date2ts(task_submit_date)
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    #test
    now_ts = datetime2ts('2013-09-08')
    date_ts = datetime2ts(now_date)
    segment = int((now_ts - date_ts) / 900) + 1
    end_ts = date_ts + segment * 900
    #every search time-range: 4 hour----bulk action to search
    begin_ts = start_ts

    while True:
        if begin_ts >= end_ts:
            break
        compute_ts = ts2date(begin_ts)
        #print 'compute ts:', compute_ts
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
                #print 'compute_count'
                count_dict = json.loads(result_item['count'])
                for sensitive in count_dict:
                    count_key = 'count_' + sensitive
                    result[count_key][str(timestamp)] = count_dict[sensitive]
                #attr_sentiment
                #print 'compute_sentiment'
                sensitive_sentiment_dict = json.loads(result_item['sentiment'])
                for sensitive in sensitive_sentiment_dict:
                    sentiment_dict = sensitive_sentiment_dict[sensitive]
                    for sentiment in sentiment_dict:
                        sentiment_key = 'sentiment_'+sensitive+'_'+sentiment
                        result[sentiment_key][str(timestamp)] = sentiment_dict[sentiment]
                #attr_sensitive_score
                #print 'compute_sensitive_word'
                if 'sensitive_word' in result_item:
                    sensitive_word_dict = json.loads(result_item['sensitive_word'])
                else:
                    sensitive_word_dict = {}
                ts_word_score = 0
                for word in sensitive_word_dict:
                    #print 'word:', json.dumps(word.encode('utf-8')), word.encode('utf-8'), type(word.encode('utf-8'))
                    search_word = word.encode('utf-8')
                    #print 'search_word:', search_word, type(search_word)
                    try:
                        word_identify = json.loads(word_r.hget('sensitive_words', search_word))
                    except:
                        word_identify = [2]
                    ts_word_score += sensitive_word_dict[word] * word_identify[0]
                result['sensitive_score'][str(timestamp)] = ts_word_score
                #attr_geo
                #print 'compute geo'
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
                #print 'compute hashtag'
                if 'hashtag' in result_item:
                    sensitive_hashtag_dict = json.loads(result_item['hashtag'])
                else:
                    sensitive_hashtag_dict = {}
                    result['hashtag_0'][timestamp_date] = {}
                    result['hashtag_1'][timestamp_date] = {}
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
    peak_compute_field = ['count_0', 'count_1', 'sentiment_0_126', 'sentiment_0_127', 'sentiment_0_128',\
                          'sentiment_0_129', 'sentiment_0_130', 'sensitive_score',\
                          'sentiment_1_126', 'sentiment_1_127', 'sentiment_1_128', 'sentiment_1_129', \
                          'sentiment_1_130']
    #print 'compute_peak'
    for field in peak_compute_field:
        complement_item = complement_ts(result[field], start_ts, end_ts)
        sort_complement_item = sorted(complement_item.items(), key=lambda x:int(x[0]))
        detect_peaks_input = [item[1] for item in sort_complement_item]
        #print 'start_detect_peaks'
        result[field+'_peak'] = detect_peaks(detect_peaks_input)
        result[field] = sort_complement_item
    
    #compute abnormal evaluate
    abnormal_index_dict = compute_abnormal(result)
    #print 'abnormal_index_dict:', abnormal_index_dict
    result = dict(result, **abnormal_index_dict)

    return result


def compute_abnormal(result):
    abnormal_index_dict = {}
    #step1:compute count abnormal
    count_0_list = [item[1] for item in result['count_0']]
    count_0_peak = result['count_0_peak']
    evaluate_index_count_0 = compute_count_abnormal_index(count_0_list, count_0_peak)

    count_1_list = [item[1] for item in result['count_1']]
    count_1_peak = result['count_1_peak']
    evaluate_index_count_1 = compute_count_abnormal_index(count_1_list, count_1_peak)

    abnormal_index_dict['count_abnormal'] = evaluate_index_count_0 * 0.25 + evaluate_index_count_1 * 0.75
    
    #step2:compute sentiment abnormal
    sentiment_0_126_list = [item[1] for item in result['sentiment_0_126']]
    sentiment_0_126_peak = result['sentiment_0_126_peak']
    sentiment_0_127_list = [item[1] for item in result['sentiment_0_127']]
    sentiment_0_127_peak = result['sentiment_0_127_peak']
    sentiment_0_128_list = [item[1] for item in result['sentiment_0_128']]
    sentiment_0_128_peak = result['sentiment_0_128_peak']
    evaluate_index_sentiment_0 = compute_sentiment_abnormal_index(sentiment_0_126_list, sentiment_0_126_peak, sentiment_0_127_list, sentiment_0_127_peak, sentiment_0_128_list, sentiment_0_128_peak)
    
    sentiment_1_126_list = [item[1] for item in result['sentiment_1_126']]
    sentiment_1_126_peak = result['sentiment_1_126_peak']
    sentiment_1_127_list = [item[1] for item in result['sentiment_1_127']]
    sentiment_1_127_peak = result['sentiment_1_127_peak']
    sentiment_1_128_list = [item[1] for item in result['sentiment_1_128']]
    sentiment_1_128_peak = result['sentiment_1_128_peak']
    evaluate_index_sentiment_1 = compute_sentiment_abnormal_index(sentiment_1_126_list, sentiment_1_126_peak, sentiment_1_127_list, sentiment_1_127_peak, sentiment_1_128_list, sentiment_1_128_peak)

    abnormal_index_dict['sentiment_abnormal'] = evaluate_index_sentiment_0 * 0.25 + evaluate_index_sentiment_1 * 0.75

    #step3:compute sensitive count abnormal
    sensitive_score_list = [item[1] for item in result['sensitive_score']]
    sensitive_peak = result['sensitive_score_peak']
    abnormal_index_dict['sensitive_abnormal'] = compute_sensitive_abnormal_index(sensitive_score_list, sensitive_peak)
    
    #step4:compute hashtag count abnormal
    hashtag_0_dict = [result['hashtag_0'][date] for date in result['hashtag_0']] # [{date1_dict}, {date2_dict}]
    hashtag_1_dict = [result['hashtag_1'][date] for date in result['hashtag_1']]
    abnormal_index_dict['hashtag_abnormal'] = compute_hashtag_abnormal_index(hashtag_0_dict, hashtag_1_dict)
    
    #step5:compute geo abnormal
    geo_0_dict = [result['geo_0'][date] for date in result['geo_0']]
    geo_1_dict = [result['geo_1'][date] for date in result['geo_1']]
    abnormal_index_dict['geo_abnormal'] = compute_hashtag_abnormal_index(geo_0_dict, geo_1_dict)

    return abnormal_index_dict

#compute hashtag abnormal index
def compute_hashtag_abnormal_index(hashtag_0_dict, hashtag_1_dict):
    abnormal_index = 0
    date_len = len(hashtag_0_dict)
    for item in range(0, date_len):
        date_item_0_list = hashtag_0_dict[item].values()
        if date_item_0_list==[]:
            date_item_0_max = 0
            date_item_0_ave = 0
        else:
            date_item_0_max = max(date_item_0_list)
            date_item_0_ave = float(sum(date_item_0_list)) / len(date_item_0_list)
        date_item_1_list = hashtag_1_dict[item].values()
        if date_item_1_list==[]:
            date_item_1_max = 0
            date_item_1_ave = 0
        else:
            date_item_1_max = max(date_item_1_list)
            date_item_1_ave = float(sum(date_item_1_list)) / len(date_item_1_list)
        if date_item_1_ave > 3*date_item_0_ave:
            abnormal_index += 1
        if date_item_1_max > 2*date_item_1_ave:
            abnormal_index += 1.5
        if date_item_0_max > 2*date_item_0_ave:
            abnormal_index += 0.5
    abnormal_index = float(abnormal_index) / date_len
    return abnormal_index

#compute sensitive count abnormal
def compute_sensitive_abnormal_index(sensitive_score_list, sensitive_peak):
    abnormal_index= 0
    ave_sensitive_score = float(sum(sensitive_score_list)) / len(sensitive_score_list)
    max_sensitive_score = max(sensitive_score_list)
    peak_sensitive_list = [sensitive_score_list[peak_location] for peak_location in sensitive_peak]
    ave_peak_sensitive = float(sum(peak_sensitive_list)) / len(peak_sensitive_list)
    if max_sensitive_score >= 9:
        abnormal_index += 1
    if ave_peak_sensitive / ave_sensitive_score >= 2:
        abnormal_index += 1
    if ave_peak_sensitive >= 3:
        abnormal_index += 1
    return abnormal_index


#compute sentiment abnormal index
def compute_sentiment_abnormal_index(sentiment_126, sentiment_126_peak, sentiment_127, sentiment_127_peak, sentiment_128, sentiment_128_peak):
    abnormal_index = 0
    ave_sentiment_126 = float(sum(sentiment_126)) / len(sentiment_126)
    ave_sentiment_127 = sum(sentiment_127) / len(sentiment_127)
    max_sentiment_127_count = max(sentiment_127)
    ave_sentiment_128 = float(sum(sentiment_128)) / len(sentiment_128)
    max_sentiment_128_count = max(sentiment_128)
    if max_sentiment_127_count >= 25:
        abnormal_index += 1
    if max_sentiment_128_count >= 25:
        abnormal_index += 1
    if ave_sentiment_128 / ave_sentiment_126 >= 2 or ave_sentiment_128/ ave_sentiment_126 >= 2:
        abnormal_index += 1

    return abnormal_index


#compute count abnormal index
def compute_count_abnormal_index(input_list, peak_list):
    abnormal_index = 0
    max_count = max(input_list)
    ave_count = float(sum(input_list)) / len(input_list)
    peak_count_list = [input_list[peak_location] for peak_location in peak_list]
    ave_peak_count = float(sum(peak_count_list)) / len(peak_count_list)
    if max_count >= 25:
        abnormal_index += 1
    if ave_peak_count / ave_count >= 3:
        abnormal_index += 1
    if ave_count >= 10:
        abnormal_index += 1
    return abnormal_index

'''
# compute abnormal from time trend of one attribute and peak
def compute_abnormal(field, detect_peaks_input, peak_list):
    evaluate_index = 0
    if field in ['count_0','count_1']:
        max_count = max(detect_peaks_input)
        ave_count = sum(detect_peaks_input) / len(detect_peaks_input)
        peak_count_list = [detect_peaks_input[peak_location] for peak_location in peak_list]
        ave_peak_count = sum(peak_count_list) / len(peak_count_list)
        if max_count >= 25:
            evaluate_index += 1
        if ave_peak_count / ave_count >= 3:
            evaluate_index += 1
        evaluate_key = field

    elif field in ['sentiment_0_127', 'sentiment_0_128', 'sentiment_0_129', 'sentiment_1_127', 'sentiment_1_128', 'sentiment_1_129']:
        max_count = max(detect_peaks_input)
        ave_count = sum(detect_peaks_input) / len(detect_peaks_input)
        peak_count_list = [detect_peaks_input[peak_location] for peak_location in peak_list]
        ave_peak_count  = sum(peak_count_list) / len(peak_count_list)
        
        
    return evaluate_index
'''

# add ts with value is 0
def complement_ts(result_dict,start_ts, end_ts):
    ts = start_ts
    time_segment = 900
    #print 'start_ts:', ts2date(ts)
    #print 'end_ts:', ts2date(end_ts)
    #print 'result_dict:', result_dict
    while True:
        if ts > end_ts:
            break
        #print 'ts:', ts2date(ts)
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

    select_top_dict = {} # {uid:[ave_retweet_count, ave_peak_retweet_count]}
    #select union top5 ave_retweet_count and top5 ave_peak_retweet_count

    for user in task_user:
        result[user+'_comment'] = {}
        result[user+'_retweet'] = {}
        comment_retweet_dict = monitor_r.hgetall(user)
        for item in comment_retweet_dict:
            item_type_ts = item.split('_')
            item_type = item_type_ts[0]
            item_ts = item_type_ts[1]
            result[user+'_'+item_type][item_ts] = int(comment_retweet_dict[item])
        # use to detect peaks
        comment_dict = result[user+'_comment']
        complement_comment_dict = complement_ts(comment_dict, start_ts, end_ts)
        sort_comment_dict = sorted(complement_comment_dict.items(), key=lambda x:int(x[0]))
        detect_peaks_comment_input = [item[1] for item in sort_comment_dict]
        #print 'detect_peaks_comment_input:', detect_peaks_comment_input
        result[user+'_comment_peak'] = detect_peaks(detect_peaks_comment_input)

        retweet_dict = result[user+'_retweet']
        complement_retweet_dict = complement_ts(retweet_dict, start_ts, end_ts)
        sort_retweet_dict = sorted(complement_retweet_dict.items(), key=lambda x:int(x[0]))
        detect_peaks_retweet_input = [item[1] for item in sort_retweet_dict]
        result[user+'_retweet_peak'] = detect_peaks(detect_peaks_retweet_input)
        
        ave_retweet_count = sum(detect_peaks_retweet_input) / len(detect_peaks_retweet_input)
        peak_count_list = [detect_peaks_retweet_input[peak_location] for peak_location in result[user+'_retweet_peak']]
        ave_peak_count = sum(peak_count_list) / len(peak_count_list)
        select_top_dict[user] = [ave_retweet_count, ave_peak_count]
    
    #select union top5
    sort_select_top_count_dict = sorted(select_top_dict.items(), key=lambda x:x[1][0], reverse=True)
    top5_count_user_list = sort_select_top_count_dict[:5]
    top5_count_user = [item[0] for item in top5_count_user_list]
    sort_select_top_peak_dict = sorted(select_top_dict.items(), key=lambda x:x[1][1], reverse=True)
    top5_peak_user_list = sort_select_top_peak_dict[:5]
    top5_peak_user = [item[0] for item in top5_peak_user_list]
    union_user = list(set(top5_count_user) & set(top5_peak_user))
    new_result = {}
    for user in union_user:
        new_result[user+'_retweet'] = result[user+'_retweet']
        new_result[user+'_retweet_peak'] = result[user+'_retweet_peak']
        new_result[user+'_comment'] = result[user+'_comment']
        new_result[user+'_comment_peak'] = result[user+'_comment_peak']
    
    new_result['profile'] = get_top_user_profile(union_user)

    #compute abnormal index
    new_result['abnormal_index'] = compute_comment_retweet_abnormal(new_result, union_user)

    return new_result

# use to compute retweet/comment abnormal for a monitor_task
def compute_comment_retweet_abnormal(new_result, union_user):

    abnormal_index = 0
    retweet_abnormal_index = 0
    comment_abnormal_index = 0
    for user in union_user:
        retweet_dict = new_result[user+'_retweet']
        retweet_list = [retweet_dict[item] for item in retweet_dict]
        retweet_peak_location = new_result[user+'_retweet_peak']
        retweet_abnormal_index += compute_user_comment_retweet_abnormal(retweet_list, retweet_peak_location)
        comment_dict = new_result[user+'_comment']
        comment_list = [comment_dict[item] for item in comment_dict]
        comment_peak_location = new_result[user+'_comment_peak']
        comment_abnormal_index += compute_user_comment_retweet_abnormal(comment_list, comment_peak_location)
    
    abnormal_index = float(retweet_abnormal_index) / len(union_user) * 0.7 + float(comment_abnormal_index) / len(union_user) * 0.3
    #print 'retweet_abnormal_index, comment_abnormal_index:', retweet_abnormal_index, comment_abnormal_index

    return abnormal_index


# use to compute retweet/comment abnormal index for every body
def compute_user_comment_retweet_abnormal(input_list, peak_location):
    abnormal_index = 0
    ave_count = float(sum(input_list)) / len(input_list)
    max_count = sum(input_list)
    peak_list = [input_list[peak] for peak in peak_location]
    ave_peak_count = float(sum(peak_list)) / len(peak_list)
    #print 'compute user abnormal:', ave_count, max_count, ave_peak_count
    if ave_count >= 20:
        abnormal_index += 1
    if max_count >= 10000:
        abnormal_index += 1
    if float(ave_peak_count) / ave_count >= 1.5:

        abnormal_index += 1

    return abnormal_index

# get top user profile imagein
def get_top_user_profile(union_user):
    result = {} # result[user] = [uname, imgin_url]
    for user in union_user:
        try:
            user_item = es_user_profile.get(index=profile_index_name, doc_type=profile_index_type,\
                                            id=uid)['_source']
        except:
            user_item = None
        if not user_item:
            result[user] = [u'未知', '']
        else:
             uname = user_item['nick_name']
             photo_url = user_item['photo_url']
             result[user] = [uname, photo_url]

    return result



# get monitor task user inner group polarization
# time range: the latest 7 day
# output: time is in reversed order
def get_network(task_exist):
    task_name = task_exist['task_name']
    submit_date = task_exist['submit_date']
    submit_ts = date2ts(submit_date)

    time_segment = 24*3600
    now_ts = time.time()
    now_date = ts2datetime(now_ts)
    now_date_ts = datetime2ts(now_date)
    #test
    now_date_ts = datetime2ts('2013-09-07')
    iter_date_ts = now_date_ts
    iter_count = 1
    date_list = []
    top_list_dict = {}
    while True:
        if iter_count >= 8 or iter_date_ts < submit_ts:
            break
        iter_date = ts2datetime(iter_date_ts)
        date_list.append(iter_date)
        key = 'inner_' + str(iter_date)
        try:
            task_date_result = es.get(index=monitor_index_name, doc_type=task_name, id=key)['_source']
        except:
            task_date_result = {}
        #print 'task_name, key, task_date_result:', task_name, key, task_date_result
        iter_field = ['top1', 'top2', 'top3', 'top4', 'top5']
        for field in iter_field:
            user_count_item = json.loads(task_date_result[field])
            uid = user_count_item[0]
            uname = uid2uname(uid)
            count = user_count_item[1]
            try:
                top_list_dict[field].append([uid, uname, count])
            except:
                top_list_dict[field] = [[uid, uname, count]]
        
        iter_date_ts -= time_segment
        # get inner-retweet group from es---field: inner_graph
        '''
        try:
            inner_graph = json.loads(task_date_result['inner_graph'])
        except:
            inner_graph = {}
        '''

    abnormal_index = compute_inner_polarization(top_list_dict)
    
    return [date_list, top_list_dict, abnormal_index]


# compute abnormal about inner polarization
def compute_inner_polarization(top_list_dict):
    abnormal_index = 0
    #print 'top_list_dict:', top_list_dict
    top1_user_list = [item[0] for item in top_list_dict['top1']]
    top2_user_list = [item[0] for item in top_list_dict['top2']]
    top1_user_list.extend(top2_user_list)
    #print 'top1_user_list:', top1_user_list
    top_user_set = set(top1_user_list)
    #print 'top_user_set:', top_user_set
    if len(top_user_set) <= 3:
        abnormal_index += 1
    user_count_list = []
    for field in top_list_dict:
        field_user_count = [item[2] for item in top_list_dict[field]]
        user_count_list.extend(field_user_count)
    #print 'user_count_list:', user_count_list
    max_user_count = max(user_count_list)
    ave_user_count = float(sum(user_count_list)) / len(user_count_list)
    if max_user_count >= 0.3:
        abnormal_index += 1
    if ave_user_count >= 0.1:
        abnormal_index += 1

    return abnormal_index

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

# use to get weibo about inner_group_polarization
def get_inner_top_weibo(task_name, date, uid):
    result = []
    # step1: identify the task exist
    # step2: search weibo from monitor_user_text by condition: task_user, date
    task_exist = identify_task(task_name)
    if not task_exist:
        return 'the task is not exist'
    task_user = task_exist['uid_list']
    if uid not in task_user:
        return 'the user is not exist'
    end_ts = datetime2ts(date)
    time_segment = 24*3600
    start_ts = end_ts - time_segment
    query_body = []
    #term search: uid
    query_body.append({'term': uid})
    #range search: date-24*3600, date
    query_body.append({'range':{'timestamp': {'from': start_ts, 'to': end_ts}}})
    try:
        weibo_result = es.search(index=text_index_name, doc_type=text_index_type, \
                body={'query':{'bool':{'must': query_body}}, 'sort':[{'timestamp':{'order':'asc'}}], 'size':10000})['hits']['hits']
    except Exception, e:
        raise e
    uname = uid2uname(uid)

    for weibo_dict in weibo_result:
        weibo_item = weibo_dict['_source']
        text = weibo_item['text']
        timestamp = weibo_item['timestamp']
        weibo_date = ts2date(timestamp)
        geo = weibo_item['geo']
        result.append([uid, uname, geo, weibo_date, text])

    return result

# get weibo of one hashtag by condition: task_user, hashtag, timestamp
def get_hashtag_weibo(task_name, hashtag, timestamp):
    results = []
    #step1: identify task exist
    #step2: search weibo from monitor_user_text by condition: task user, hashtag, timestamp
    task_exist = identify_task(task_name)
    if not task_exist:
        return 'task is not exist'
    task_user = task_exist['uid_list']
    query_body = []
    #multi-search: task user
    nest_body_list = []
    for uid in task_user:
        nest_body_list.append({'term': {'uid': uid}})
    query_body.append({'bool': {'should': nest_body_list}})
    #range-search: timestamp timestamp+day
    query_body.append({'range': {'timestmap':{'from': timestamp, 'to': timestamp + 24*3600}}})
    #wildcard-search: hashtag
    query_body.append({'wildcard':{'hashtag': '*' + hashtag + '*'}})
    try:
        weibo_dict_list = es.search(index=text_index_name, doc_type=text_index_type, \
                body={'query':{'bool':{'must': query_body}}, 'sort':[{'timestamp': {'order': 'asc'}}], 'size':10000})['hits']['hits']
    except Exception, e:
        raise e
    for weibo_dict in weibo_dict_list:
        weibo_item = weibo_dict['_source']
        uid = weibo_item['uid']
        uname = uid2uname(uid)
        text = weibo_item['text']
        timestamp = weibo_item['timestamp']
        date = ts2date(timestamp)
        results.append([uid, uname, date, text])
    
    return results

