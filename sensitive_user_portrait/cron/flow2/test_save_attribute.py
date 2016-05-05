# -*- coding: UTF-8 -*-
'''
test save in a redis not in the cluster_redis
'''
import sys
import csv
import json
import time
import redis
reload(sys)
sys.path.append('../../')
from time_utils import ts2datetime, datetime2ts
from global_utils import redis_ip
from global_utils import redis_activity
from global_utils import redis_cluster



# save redis as Date:{uid1:'{str(at_uid1):count1,... }', uid2:'str(at_uid2):count2,...'}
def save_at(uid, at_uid, timestamp, sensitive):
    date = ts2datetime(timestamp)
    ts = datetime2ts(date)
    key = str(uid)
    ruid_count_dict = dict()
    sensitive_ruid_count_dict = dict()
    ruid_count_string = redis_cluster.hget('at_'+str(ts), str(uid))
    if ruid_count_string:
        ruid_count_dict = json.loads(ruid_count_string)
        if ruid_count_dict.has_key(str(at_uid)):
            ruid_count_dict[str(at_uid)] += 1
        else:
            ruid_count_dict[str(at_uid)] = 1
    else:
        ruid_count_dict[str(at_uid)] = 1
    redis_cluster.hset('at_'+str(ts), str(uid), json.dumps(ruid_count_dict))


    if sensitive:
        sensitive_ruid_count_string = redis_cluster.hget('sensitive_at_'+str(ts), str(uid))
        if sensitive_ruid_count_string:
            sensitive_ruid_count_dict = json.loads(sensitive_ruid_count_string)
            if sensitive_ruid_count_dict.has_key(str(at_uid)):
                sensitive_ruid_count_dict[str(at_uid)] += 1
            else:
                sensitive_ruid_count_dict[str(at_uid)] = 1
        else:
            sensitive_ruid_count_dict[str(at_uid)] = 1
        redis_cluster.hset('sensitive_at_'+str(ts), str(uid), json.dumps(sensitive_ruid_count_dict))


# save redis as Date:{uid1:'{ip:count...}', uid2:'{ip:count....}'}
def save_city(uid, ip, timestamp, sensitive):
    date = ts2datetime(timestamp)
    ts = datetime2ts(date)
    key = str(uid)
    ip_count_dict = dict()
    sensitive_ip_count_dict = dict()
    ip_count_string = redis_ip.hget('ip_'+str(ts), str(uid))
    if ip_count_string:
        ip_count_dict = json.loads(ip_count_string)
        if ip_count_dict.has_key(str(ip)):
            ip_count_dict[str(ip)] += 1
        else:
            ip_count_dict[str(ip)] = 1
    else:
        ip_count_dict[str(ip)] = 1
    redis_ip.hset('ip_'+str(ts), str(uid), json.dumps(ip_count_dict))

    if sensitive:
        sensitive_ip_count_string = redis_ip.hget('sensitive_ip_'+str(ts), str(uid))
        if sensitive_ip_count_string:
            sensitive_ip_count_dict = json.loads(sensitive_ip_count_string)
            if sensitive_ip_count_dict.has_key(str(ip)):
                sensitive_ip_count_dict[str(ip)] += 1
            else:
                sensitive_ip_count_dict[str(ip)] = 1
        else:
            sensitive_ip_count_dict[str(ip)] = 1
        redis_ip.hset('sensitive_ip_'+str(ts), str(uid), json.dumps(sensitive_ip_count_dict))


# save redis as 'activity_' + Date:{uid1:'{}', uid2:'{}'}        
def save_activity(uid, timestamp, time_segment, sensitive):
    date = ts2datetime(timestamp)
    ts = datetime2ts(date)
    key = str(ts)
    activity_count_dict = dict()
    sensitive_activity_count_dict = dict()
    activity_count_string = redis_activity.hget('activity_' + key, str(uid))
    if activity_count_string:
        activity_count_dict = json.loads(activity_count_string)
        if activity_count_dict.has_key(str(time_segment)):
            activity_count_dict[str(time_segment)] += 1
        else:
            activity_count_dict[str(time_segment)] = 1
    else:
        activity_count_dict[str(time_segment)] = 1
    redis_activity.hset('activity_' + key, str(uid), json.dumps(activity_count_dict))

    if sensitive:
        sensitive_activity_count_string = redis_activity.hget('sensitive_activity_' + key, str(uid))
        if sensitive_activity_count_string:
            sensitive_activity_count_dict = json.loads(sensitive_activity_count_string)
            if sensitive_activity_count_dict.has_key(str(time_segment)):
                sensitive_activity_count_dict[str(time_segment)] += 1
            else:
                sensitive_activity_count_dict[str(time_segment)] = 1
        else:
            sensitive_activity_count_dict[str(time_segment)] = 1
        redis_activity.hset('sensitive_activity_' + key, str(uid), json.dumps(sensitive_activity_count_dict))


def cal_hashtag_work(uid, hashtag_list, timestamp, sensitive):
    date = ts2datetime(timestamp)
    ts = datetime2ts(date)
    key = str(uid)

    hashtag_dict = {}
    sensitive_hashtag_dict = dict()
    for hashtag in hashtag_list:
        try:
            hashtag_dict[hashtag] += 1
        except:
            hashtag_dict[hashtag] = 1
    hashtag_count_string = redis_cluster.hget('hashtag_'+str(ts), str(uid))
    if hashtag_count_string:
        hashtag_count_dict = json.loads(hashtag_count_string)
        for item in hashtag_list:
            if hashtag_count_dict.has_key(item):
                hashtag_count_dict[item] += 1
            else:
                hashtag_count_dict[item] = 1
    else:
        hashtag_count_dict = hashtag_dict
    redis_cluster.hset('hashtag_'+str(ts), str(uid), json.dumps(hashtag_count_dict))

    if sensitive:
        sensitive_hashtag_count_string = redis_cluster.hget('sensitive_hashtag_'+str(ts), str(uid))
        if sensitive_hashtag_count_string:
            sensitive_hashtag_count_dict = json.loads(sensitive_hashtag_count_string)
            for hashtag in hashtag_list:
                if sensitive_hashtag_count_dict.has_key(hashtag):
                    sensitive_hashtag_count_dict[hashtag] += 1
                else:
                    sensitive_hashtag_count_dict[hashtag] = 1
        else:
            sensitive_hashtag_count_dict = hashtag_dict

        redis_cluster.hset('sensitive_hashtag_'+str(ts), str(uid), json.dumps(sensitive_hashtag_count_dict))


