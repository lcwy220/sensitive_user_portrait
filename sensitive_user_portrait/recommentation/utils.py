# -*- coding:utf-8 -*-

import redis
import sys
import math
import time
import datetime
import json
import IP
from elasticsearch import Elasticsearch
from sensitive_user_portrait.global_utils import R_RECOMMENTATION as r
from sensitive_user_portrait.global_utils import redis_cluster
from sensitive_user_portrait.global_utils import redis_ip, redis_activity
#from sensitive_user_portrait.global_utils import es_user_profile as es_cluster
from sensitive_user_portrait.global_utils import es_user_profile, es_sensitive_history
from sensitive_user_portrait.global_utils import ES_CLUSTER_FLOW2 as es_cluster
from sensitive_user_portrait.global_utils import ES_CLUSTER_FLOW1 as es_bci
from sensitive_user_portrait.global_utils import es_sensitive_user_portrait,es_sensitive_history
from sensitive_user_portrait.time_utils import ts2datetime, datetime2ts
from sensitive_user_portrait.parameter import pre_influence_index, influence_doctype, RUN_TYPE, WORK_TYPE,ip_index_pre, sen_ip_index_pre, act_index_pre, sen_act_index_pre, DAY

r_cluster = redis_cluster

def get_top_value(key, es, index_name, index_type):
    query_body = {
        "query":{
            "match_all":{}
        },
        "size":1,
        "sort":{key: {"order":"desc"}}
    }

    try:
        result = es.search(index=index_name, doc_type=index_type, body=query_body, _source=False, fields=[key])["hits"]["hits"]
        top_value = result[0]['fields'][key][0]
    except Exception, reason:
        print Exception, reason
        raise reason
    return top_value



# obtain user detail information, such as uid,nickname,location,fansnum,statusnum,influence,weibo_mid
def get_sensitive_user_detail(uid_list, date, sensitive):
    es_cluster = es_user_profile
    ts = datetime2ts(date)
    results = []
    index_name = pre_influence_index + str(date).replace('-','') # index_name:20130901
    user_bci_results = es_bci.mget(index=index_name, doc_type='bci', body={'ids':uid_list}, _source=False, fields=['user_index'])['docs']
    user_profile_results = es_user_profile.mget(index="weibo_user", doc_type="user", body={"ids":uid_list}, _source=True)['docs']
    top_influnce_value = get_top_value("user_index", es_bci, index_name, "bci")
    for i in range(0, len(uid_list)):
        personal_info = ['']*6
        uid = uid_list[i]
        personal_info[0] = uid_list[i]
        personal_info[1] = uid_list[i]
        if user_profile_results[i]['found']:
            profile_dict = user_profile_results[i]['_source']
            uname = profile_dict['nick_name']
            if uname:
                personal_info[1] = uname
            personal_info[2] = profile_dict['user_location']
            personal_info[3] = profile_dict['fansnum']
            personal_info[4] = profile_dict['statusnum']
        if user_bci_results[i]['found']:
            try:
                tmp_bci = user_bci_results[i]['fields']['user_index'][0]
                influence = math.log(tmp_bci/float(top_influnce_value)*9+1, 10)*100
                personal_info[5] = influence
            except:
                personal_info[5] = 0
        else:
            personal_info[5] = 0
        if sensitive:
            sensitive_words = redis_cluster.hget('sensitive_' + str(ts), str(uid))
            if sensitive_words:
                sensitive_dict = json.loads(sensitive_words)
                personal_info.append(sensitive_dict.keys())
            else:
                personal_info.append([])
        else:
            personal_info.append([])
        results.append(personal_info)
    return results


# show recommend in, sensitive user, date
# 
# date = 20130901
def recommend_in_sensitive(date):
    sensitive_name = "recomment_" + str(date) + "_sensitive"
    compute_name = "compute_" + str(date)
    re_sen_set = r.hkeys(sensitive_name) # 敏感人物推荐
    iden_in_set = r.hkeys(compute_name) # 已经入库用户
    if not re_sen_set:
        return [] # 那一天不存在数据
    uid_list = list(set(re_sen_set) - set(iden_in_set))
    sensitive = 1
    work_date = ts2datetime(datetime2ts(date)-DAY)
    if uid_list:
        results = get_sensitive_user_detail(uid_list, work_date, sensitive)
    else:
        results = []
    return results

# show top influence user recommend
def recommend_in_top_influence(date):
    influence_name = "recomment_" + date + "_influence"
    identify_in_name = "compute_" + str(date)
    re_inf_set = r.hkeys(influence_name)
    iden_in_set = r.hkeys(identify_in_name) # 已经入库用户

    if not re_inf_set:
        return []
    else:
        uid_list = list(set(re_inf_set) - set(iden_in_set))
    sensitive = 0
    work_date = ts2datetime(datetime2ts(date)-DAY)
    if uid_list:
        results = get_sensitive_user_detail(uid_list, work_date, sensitive)
    else:
        results = []
    return results

# get user hashtag
def get_user_hashtag(uid):
    user_hashtag_dict = {}
    sensitive_user_hashtag_dict = {}
    if RUN_TYPE:
        now_ts = time.time()
        now_date = ts2datetime(now_ts) # 2015-09-22
    else:
        now_date = "2013-09-08"
    ts = datetime2ts(now_date)

    #test
    #ts = datetime2ts('2013-09-08')
    for i in range(1,8):
        ts = ts - 3600*24
        results = r_cluster.hget('hashtag_'+str(ts), uid)
        sensitive_results = r_cluster.hget('sensitive_hashtag_'+str(ts), uid)
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
    if RUN_TYPE:
        now_ts = time.time()
        now_date = ts2datetime(now_ts) # 2015-09-22
    else:
        now_date = "2013-09-08"
    ts = datetime2ts(now_date)

    #test
    #ts = datetime2ts('2013-09-08')
    for i in range(1,8):
        ts = ts - 3600*24
        date = ts2datetime(ts).replace('-','')
        results = r_cluster.hget('sensitive_'+str(ts), uid)
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
    if RUN_TYPE:
        now_ts = time.time()
        now_date = ts2datetime(now_ts) # 2015-09-22
    else:
        now_date = "2013-09-08"
    ts = datetime2ts(now_date)

    for i in range(1,8):
        ts = ts - 3600*24
        date = ts2datetime(ts)
        if WORK_TYPE == 0:
            index_name = ip_index_pre + str(date)
            sensitive_index_name = sen_ip_index_pre + str(date)
            exist_bool = es_cluster.indices.exists(index=index_name)
            sensitive_exist_bool = es_cluster.indices.exists(index=sensitive_index_name)
            if exist_bool:
                try:
                    tmp_ip_result = es_cluster.get(index=index_name, doc_type="ip", id=uid)['_source']
                    results = tmp_ip_result['ip_dict']
                except:
                    results = dict()
            else:
                results = dict()
            if sensitive_exist_bool:
                try:
                    tmp_sensitive_ip_result = es_cluster.get(index=sensitive_index_name, doc_type="sensitive_ip", id=uid)['_source']
                    sensitive_results = tmp_sensitive_ip_result['sensitive_ip_dict']
                except:
                    sensitive_results = dict()
            else:
                sensitive_results = dict()
        else:
            results = redis_ip.hget('ip_'+str(ts), uid)
            sensitive_results = redis_ip.hget('sensitive_ip'+str(ts), uid)
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
    if RUN_TYPE:
        now_ts = time.time()
        now_date = ts2datetime(now_ts) # 2015-09-22
    else:
        now_date = "2013-09-08"
    ts = datetime2ts(now_date)

    #test
    #ts = datetime2ts('2013-09-08')
    timestamp = ts
    return_results = dict()
    return_sensitive_results = {}
    for i in range(1,8):
        ts = timestamp -24*3600*i
        date = ts2datetime(ts)
        if WORK_TYPE == 0:
            index_name = act_index_pre + date
            sensitive_index_name = sen_act_index_pre + date
            exist_bool = es_cluster.indices.exists(index=index_name)
            sensitive_exist_bool = es_cluster.indices.exists(index=sensitive_index_name)
            if exist_bool:
                try:
                    tmp_act_result = es_cluster.get(index=index_name, doc_type="activity", id=uid)['_source']
                    results = tmp_act_result['activity_dict']
                except:
                    results = dict()
            else:
                results = dict()
            if sensitive_exist_bool:
                try:
                    tmp_sensitive_act_result = es_cluster.get(index=sensitive_index_name, doc_type="sensitive_activity", id=uid)['_source']
                    sensitive_results = tmp_sensitive_ip_result['sensitive_activity_dict']
                except:
                    sensitive_results = dict()
            else:
                sensitive_results = dict()
        else:
            results = redis_activity.hget('activity_'+str(ts), uid)
            sensitive_results = redis_activity.hget('sensitive_activity_'+str(ts), uid)
        if results:
            result_dict = json.loads(results)
            key_set = set(result_dict.keys())
            for key in result_dict.keys():
                return_results[int(key)*900+ts] = result_dict[key]
        else:
            pass
        if sensitive_results:
            sensitive_result_dict = json.loads(sensitive_results)
            for key in sensitive_result_dict.keys():
                return_sensitive_results[int(key)*900+ts] = sensitive_result_dict[key]
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
                if seg_time in return_results:
                    num += return_results[seg_time]
            trend_dict[base_time] = num

    sensitive_trend_dict = {}
    for i in range(1,8):
        ts = timestamp - i*24*3600
        for j in range(0,6):
            base_time = ts + j*900*16
            num = 0
            for k in range(16):
                seg_time = base_time + k*900
                if seg_time in return_sensitive_results:
                    num += return_sensitive_results[seg_time]
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
        uid = item[1]
        status = str(item[2])
        source = str(item[3])
        if int(source) == 1:
            r.hset('identify_in_sensitive_'+str(date), uid, status) # identify in user_list and compute status
            sensitive_list.add(uid)
        elif int(source) == 2:
            r.hset('identify_in_influence_'+str(date), uid, status)
            influence_list.add(uid)
        r.hset('compute', uid, json.dumps([date, status]))

    """
    sensitive_results = r.hget('recommend_sensitive', date)
    if sensitives_results:
        sensitive_results = json.loads(sensitive_results)
        revise_set = set(sensitive_results) - sensitive_list
        if revise_set:
            r.hset('recommend_sensitive', date, json.dumps(list(revise_set)))
        else:
            r.hdel('recommend_sensitive', date)
    influence_results = r.hget('recommend_influence', date)
    if influence_results and influence_results != []:
        influence_results = json.loads(influence_results)
        revise_set = set(influence_results) - influence_list
        if revise_set:
            r.hset('recommend_influence', date, json.dumps(list(revise_set)))
        else:
            r.hdel('recommend_influence', date)

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
    """
    return '1'


def show_in_history(date):
    results = []
    sensitive_uid_list = []
    influence_uid_list = []
    sen_iden_in_name = "identify_in_sensitive_" + str(date)
    inf_iden_in_name = "identify_in_influence_" + str(date)
    sen_iden_in_results = r.hgetall(sen_iden_in_name)
    inf_iden_in_results = r.hgetall(inf_iden_in_name)
    print inf_iden_in_results
    print sen_iden_in_results
    sensitive_uid_list = sen_iden_in_results.keys()
    influence_uid_list = inf_iden_in_results.keys()
    #compute_results = r.hgetall('compute')
    results = []
    work_date = ts2datetime(datetime2ts(date)-DAY)
    print work_date

    if sensitive_uid_list:
        sensitive_results = get_sensitive_user_detail(sensitive_uid_list, work_date, 1)
    else:
        sensitive_results = []
    print sensitive_uid_list
    for item in sensitive_results:
        uid = item[0]
        status = sen_iden_in_results[uid]
        item.append(status)
        results.append(item)

    if influence_uid_list:
        influence_results = get_sensitive_user_detail(influence_uid_list, work_date, 0)
    else:
        influence_results = []
    for item in influence_results:
        uid = item[0]
        status = inf_iden_in_results[uid]
        item.append(status)
        results.append(item)

    sorted_results = sorted(results, key=lambda x:x[5], reverse=True)
    print results
    return sorted_results

