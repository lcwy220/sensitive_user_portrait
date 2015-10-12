# -*- coding:utf-8 -*-

import redis
import sys
import time
import datetime
import json
import IP
from elasticsearch import Elasticsearch
from sensitive_user_portrait.global_utils import R_RECOMMENTATION as r
from sensitive_user_portrait.global_utils import R_CLUSTER_FLOW2 as r_cluster
from sensitive_user_portrait.global_utils import ES_CLUSTER_FLOW1 as es_cluster
from sensitive_user_portrait.global_utils import es_user_profile
from sensitive_user_portrait.global_utils import es_sensitive_user_portrait
from sensitive_user_portrait.time_utils import ts2datetime, datetime2ts

# obtain user detail information, such as uid,nickname,location,fansnum,statusnum,influence,weibo_mid
def get_sensitive_user_detail(uid_list, date, sensitive):
    results = []
    index_name = str(date).replace('-','') # index_name:20130901
    user_bci_results = es_cluster.mget(index=index_name, doc_type='bci', body={'ids':uid_list}, _source=True)['docs']
    user_profile_results = es_user_profile.mget(index="weibo_user", doc_type="user", body={"ids":uid_list}, _source=True)['docs']
    for i in range(0, len(uid_list)):
        personal_info = ['']*6
        uid = uid_list[i]
        personal_info[0] = uid_list[i]
        if user_profile_results[i]['found']:
            profile_dict = user_profile_results[i]['_source']
            personal_info[1] = profile_dict['nick_name']
            personal_info[2] = profile_dict['user_location']
            personal_info[3] = profile_dict['fansnum']
            personal_info[4] = profile_dict['statusnum']
        if user_bci_results[i]['found']:
            personal_info[5] = user_bci_results[i]['_source'].get('user_index', 0)
        if sensitive:
            sensitive_words = r_cluster.hget('sensitive_' + index_name, str(uid))
            if sensitive_words:
                sensitive_dict = json.loads(sensitive_words)
                personal_info.append(sensitive_dict.keys())
        results.append(personal_info)
    return results


# show recommend in, sensitive user, date
# date = 20130901
def recommend_in_sensitive(date):
    date = date.replace('-','')
    results = r.hget('recommend_sensitive', date)
    if not results:
        return results # return '0'
    else:
        uid_list = json.loads(results)
    sensitive = 1
    return get_sensitive_user_detail(uid_list, date, sensitive)

# show top influence user recommend
def recommend_in_top_influence(date):
    date = date.replace('-','')
    results = r.hget('recommend_influence', date)
    if not results:
        return '0'
    else:
        uid_list = json.loads(results)
    sensitive = 0
    return get_sensitive_user_detail(uid_list, date, sensitive)

# get user hashtag
def get_user_hashtag(uid):
    user_hashtag_dict = {}
    sensitive_user_hashtag_dict = {}
    now_ts = time.time()
    now_date = ts2datetime(now_ts) # 2015-09-22
    ts = datetime2ts(now_date)

    #test
    ts = datetime2ts('2013-09-08')
    for i in range(1,8):
        ts = ts - 3600*24
        date = ts2datetime(ts).replace('-','')
        results = r_cluster.hget('hashtag_'+str(date), uid)
        sensitive_results = r_cluster.hget('sensitive_hashtag_'+str(date), uid)
        if results:
            hashtag_dict = json.loads(results)
            for hashtag in hashtag_dict:
                if user_hashtag_dict.has_key(hashtag):
                    user_hashtag_dict[hashtag] += hashtag_dict[hashtag]
                else:
                    user_hashtag_dict[hashtag] = hashtag_dict[hashtag]
        if sensitive_results:
            sensitive_hashtag_dict = json.loads(sensitive_results)
            for hashtag in sensitive_hashtag_dict:
                if sensitive_user_hashtag_dict.has_key(hashtag):
                    sensitive_user_hashtag_dict[hashtag] += sensitive_hashtag_dict[hashtag]
                else:
                    sensitive_user_hashtag_dict[hashtag] = sensitive_hashtag_dict[hashtag]
    ordinary_key_set = set(user_hashtag_dict.keys())
    sensitive_key_set = set(sensitive_user_hashtag_dict.keys())
    for key in sensitive_key_set:
        if key in ordinary_key_set:
            user_hashtag_dict[key] += sensitive_user_hashtag_dict[key]
        else:
            user_hashtag_dict[key] = sensitive_user_hashtag_dict[key]

    sort_hashtag_dict = sorted(user_hashtag_dict.items(), key=lambda x:x[1], reverse=True)
    sort_sensitive_dict = sorted(sensitive_user_hashtag_dict.items(), key=lambda x:x[1], reverse=True)
    return [sort_hashtag_dict, sort_sensitive_dict]

# get user sensitive words
def get_user_sensitive_words(uid):
    user_sensitive_words_dict = {}
    now_ts = time.time()
    now_date = ts2datetime(now_ts) # 2015-09-22
    ts = datetime2ts(now_date)

    #test
    ts = datetime2ts('2013-09-08')
    for i in range(1,8):
        ts = ts - 3600*24
        date = ts2datetime(ts).replace('-','')
        results = r_cluster.hget('sensitive_'+str(date), uid)
        if results:
            sensitive_words_dict = json.loads(results)
            for word in sensitive_words_dict:
                if user_sensitive_words_dict.has_key(word):
                    user_sensitive_words_dict[word] += sensitive_words_dict[word]
                else:
                    user_sensitive_words_dict[word] = sensitive_words_dict[word]
    sort_sensitive_words_dict = sorted(user_sensitive_words_dict.items(), key=lambda x:x[1], reverse=True)

    return sort_sensitive_words_dict


def ip2geo(ip_dict):
    city_set = set()
    geo_dict = dict()
    for ip in ip_dict:
        try:
            city = IP.find(str(ip))
            if city:
                city.encode('utf-8')
            else:
                city = ''
        except Exception, e:
            city = ''
        if city:
            len_city = len(city.split('\t'))
            if len_city == 4:
                city = '\t'.join(city.split('\t')[:2])
            try:
                geo_dict[city] += ip_dict[ip]
            except:
                geo_dict[city] = ip_dict[ip]
    return geo_dict



# get user geo
def get_user_geo(uid):
    results = []
    user_geo_result = {}
    user_ip_dict = {}
    user_ip_result = {} # ordinary ip
    user_sensitive_ip_result = {} # sensitive ip
    now_ts = time.time()
    now_date = ts2datetime(now_ts) # 2015-09-22
    ts = datetime2ts(now_date)

    #test
    ts = datetime2ts('2013-09-08')
    for i in range(1,8):
        ts = ts - 3600*24
        date = ts2datetime(ts).replace('-','')
        results = r_cluster.hget('ip_'+str(date), uid)
        sensitive_results = r_cluster.hget('sensitive_ip'+str(date), uid)
        if results:
            ip_results = json.loads(results)
            for ip in ip_results:
                if user_ip_result.has_key(ip):
                    user_ip_result[ip] += ip_results[ip]
                else:
                    user_ip_result[ip] = ip_results[ip]

        if sensitive_results:
            sensitive_ip_results = json.loads(sensitive_results)
            for ip in sensitive_ip_results:
                if user_sensitive_ip_result.has_key(ip):
                    user_sensitive_ip_result[ip] += sensitive_ip_results[ip]
                else:
                    user_sensitive_ip_result[ip] = sensitive_ip_results[ip]

    ordinary_key_set = set(user_ip_result.keys())
    sensitive_key_set = set(user_sensitive_ip_result.keys())
    for key in sensitive_key_set:
        if key in ordinary_key_set:
            user_ip_result[key] += user_sensitive_ip_result[key]
        else:
            user_ip_result[key] = user_sensitive_ip_result[key]

    user_geo_dict = ip2geo(user_ip_result)
    sorted_user_geo_dict = sorted(user_geo_dict.items(), key=lambda x:x[1], reverse=True)
    sensitive_user_geo_dict = ip2geo(user_sensitive_ip_result)
    sorted_sensitive_user_geo_dict = sorted(sensitive_user_geo_dict.items(), key=lambda x:x[1], reverse=True)


    return_list = []
    return_list = [sorted_user_geo_dict, sorted_sensitive_user_geo_dict] # total and sensitive
    return return_list


# get user time trend
def get_user_trend(uid):
    activity_dict = {}
    now_ts = time.time()
    date = ts2datetime(now_ts)
    ts = datetime2ts(date)

    #test
    ts = datetime2ts('2013-09-08')
    timestamp = ts
    results = dict()
    sensitive_results = {}
    for i in range(1,8):
        ts = timestamp -24*3600*i
        date = ts2datetime(ts).replace('-','')
        result_string = r_cluster.hget('activity_'+str(date), uid)
        sensitive_string = r_cluster.hget('sensitive_activity_'+str(date), uid)
        if result_string:
            result_dict = json.loads(result_string)
            key_set = set(result_dict.keys())
            for key in result_dict.keys():
                results[int(key)*900+ts] = result_dict[key]
        else:
            pass
        if sensitive_string:
            sensitive_result_dict = json.loads(sensitive_string)
            for key in sensitive_result_dict.keys():
                sensitive_results[int(key)*900+ts] = sensitive_result_dict[key]
        else:
            pass

    trend_dict = {}
    for i in range(1,8):
        ts = timestamp - i*24*3600
        for j in range(0,6):
            base_time = ts + j*900*16
            num = 0
            for k in range(16):
                seg_time = base_time + k*900
                if seg_time in results:
                    num += results[seg_time]
            trend_dict[base_time] = num

    sensitive_trend_dict = {}
    for i in range(1,8):
        ts = timestamp - i*24*3600
        for j in range(0,6):
            base_time = ts + j*900*16
            num = 0
            for k in range(16):
                seg_time = base_time + k*900
                if seg_time in sensitive_results:
                    num += sensitive_results[seg_time]
            sensitive_trend_dict[base_time] = num

    ordinary_key_set = set(trend_dict.keys())
    sensitive_key_set = set(sensitive_trend_dict.keys())
    for key in sensitive_key_set:
        if key in ordinary_key_set:
            trend_dict[key] += sensitive_trend_dict[key]
        else:
            trend_dict[key] = sensitive_trend_dict[key]

    sorted_dict = sorted(trend_dict.items(), key=lambda x:x[0], reverse=False)
    sorted_sensitive_dict = sorted(sensitive_trend_dict.items(), key=lambda x:x[0], reverse=False)
    return [sorted_dict, sorted_sensitive_dict] # total and sensitive


def influence_recommentation_more_information(uid):
    result = {}
    result['hashtag'] = get_user_hashtag(uid)[0]
    result['time_trend'] = get_user_trend(uid)[0]
    result['activity_geo'] = get_user_geo(uid)[0]
    return result

def sensitive_recommentation_more_information(uid):
    results = {}
    results['hashtag'] = get_user_hashtag(uid)[0]
    results['time_trend'] = get_user_trend(uid)[0]
    results['activity_geo'] = get_user_geo(uid)[0]

    return results

# preset status=3 as compute finish
def identify_in(data):
    appoint_list = []
    now_list = []
    sensitive_list = set()
    influence_list = set()
    for item in data:
        date = item[0] # 2015-09-22
        date = str(date).replace('-','')
        uid = item[1]
        status = str(item[2])
        source = str(item[3])
        if source == '1':
            r.hset('identify_in_sensitive_'+str(date), uid, status) # identify in user_list and compute status
            sensitive_list.add(uid)
        elif source == '2':
            r.hset('identify_in_influence_'+str(date), uid, status)
            influence_list.add(uid)
        if status == '1': # now
            now_list.append([uid, source])
        if status == '2': # appoint
            appoint_list.append([uid, source])

    sensitive_results = r.hget('recommend_sensitive', date)
    if sensitive_results:
        sensitive_results = json.loads(sensitive_results)
        revise_set = set(sensitive_results) - sensitive_list
        if revise_set:
            r.hset('recommend_sensitive', date, json.dumps(revise_set))
        else:
            r.hset('recommend_sensitive', date, '0')
    influence_results = r.hget('recommend_influence', date)
    if influence_results:
        influence_results = json.loads(influence_results)
        revise_set = set(influence_results) - influence_list
        if revise_set:
            r.hset('recommend_influence', date, json.dumps(revise_set))
        else:
            r.hset('recommend_influence', date, '0')

    # about compute
    compute_now_list = r.hget('compute_now', date)
    compute_appoint_list = r.hget('compute_appoint', date)
    # compute now user list
    if compute_now_list:
        now_list.extend(json.loads(compute_now_list))
        r.hset('compute_now', date, json.dumps(now_list))
    else:
        r.hset('compute_now', date, json.dumps(now_list))
    # appointted compute user list
    if compute_appoint_list:
        appoint_list.extend(json.loads(compute_appoint_list))
        r.hset('compute_appoint', date, json.dumps(appoint_list))
    else:
        r.hset('compute_appoint', date, json.dumps(appoint_list)) # finish compute, revise 'identify_in_state' uid status
    return '1'


def show_in_history(date, sensitive):
    results = []
    date = str(date).replace('-','')
    if sensitive: # sensitive user recommentation history
        sensitive_results = r.hgetall('identify_in_sensitive_'+str(date))
        if sensitive_results:
            uid_list = sensitive_results.keys()
            results = get_sensitive_user_detail(uid_list, date, 1)
            for item in results:
                item.append(sensitive_results[item[0]])
    else:
        influence_results = r.hgetall('identify_in_influence_'+str(date))
        if influence_results:
            uid_list = influence_results.keys()
            results = get_sensitive_user_detail(uid_list, date, 0)
            for item in results:
                item.append(influence_results[item[0]])

    return results

