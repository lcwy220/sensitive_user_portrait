# -*- coding:utf-8 -*-

# this file includes filter rules: 
# 1. user has been in sensitive user portrait
# 2. user is recommending but has not been in database
# 3. self_defined filter rule to select useful users

import sys
import time
import json
import csv
from elasticsearch import Elasticsearch

reload(sys)
sys.path.append('../../')
from global_utils import R_CLUSTER_FLOW2 as r_cluster
from global_utils import R_DICT, ES_DAILY_RANK, es_sensitive_user_portrait
from global_utils import R_RECOMMENTATION as r
from global_utils import RECOMMENTATION_TOPK as top_k
from time.utils import datetime2ts, ts2datetime

activity_threshold = 50
ip_threshold = 7
retweet_threshold = 20
mention_threshold = 15

filter_csv = open('./filter_uid_csv.csv', 'wb')
writer = csv.writer(filter_csv)


def filter_activity(user_set):
    results = []
    now_date = ts2datetime(time.time())
    now_date = '2013-09-08'
    ts = datetime2ts(now_date) - 24*3600
    date = ts2datetime(ts)
    timestamp = datetime2ts(date)
    ts = ts.replace('-','')
    for user in user_set:
        over_count = 0
        for i in range(0,7):
            ts = timestamp - 3600*24*i
            result = r_cluster.hget('activity_'+str(ts), str(user))
            if result:
                item_dict = json.loads(result)
                sorted_dict = sorted(item_dict.iteritems(), key=lambda asd:asd[1], reverse=True)
                if sorted_dict[0][1] > activity_threshold:
                    over_count = 1
        if over_count == 0:
            results.append(user)
        else:
            writer.writerow([user, 'activity'])

    print 'after filter activity: ', len(results)
    return results

def filter_ip(user_set):
    results = []
    now_date = ts2datetime(time.time())
    now_date = '2013-09-08'
    ts = datetime2ts(now_date) - 24*3600
    for user in user_set:
        ip_set = set()
        for i in range(0,7):
            timestamp = ts - 3600*24*i
            ip_result = r_cluster.hget('ip_'+str(ts), str(user))
            if ip_result:
                result_dict = json.loads(ip_result)
            else:
                result_dict = {}
            for ip in result_dict:
                ip_set.add(ip)
        if len(result_dict) < ip_threshold:
            results.append(user)
        else:
            writer.writerow([user, 'ip'])
    print 'after filter ip: ', len(results)
    return results

def filter_retweet_count(user_set):
    results = []
    now_date = ts2datetime(time.time())

    for user in user_set:
        retweet_set = set()
        for db_number in R_DICT:
            rr = R_DICT[db_number]
            retweet_result = rr.hgetall('retweet_'+str(user))
            for retweet_user in retweet_result:
                retweet_set.add(retweet_user)
        if len(retweet_ret) < retweet_threshold
            results.append(user)
        else:
            writer.writerow([user, 'retweet'])
    print 'after filter retweet: ', len(results)
    return results

def filter_mention(user_set):
    results = []
    now_date = ts2datetime(time.time())
    now_date = '2013-09-08'
    timestamp = datetime2ts(now_date) = 24*3600
    for user in user_set:
        mention_set = set()
        for i in range(0,7):
            ts = timestamp - 3600*24*i
            result = r_cluster.hget('at_'+str(ts), str(user))
            if result:
                item_dict = json.loads(result)
                for at_user in item_dict:
                    mention_set.add(at_user)
        if at_count < mention_threshold:
            results.append(user)
        else:
            writer.writerow([user, 'mention'])
    print 'after filter mention: ', len(results)
    return results



def filter_in(top_user_set):
    results = []
    try:
        in_results = es_sensitive_user_portrait.mget(index='user_portrait', doc_type='user', body={'ids':list(top_user_set)})
    except Exception as e:
        raise e
    filter_list = [item['_id'] for item in in_results['docs'] if item['found'] is True]
    print 'before filter in: ', len(top_user_set)
    print 'filter_list: ', len(filter_list)
    results = set(top_user_set) - set(filter_list)
    #print 'after filter in: ', len(results)

    return results

def filter_recommend(top_user_set):
    recommend_keys = r.hkeys('recommend')
    recommend_list = []
    for key in recommend_keys:
        recommend_list.extend(json.loads(r.hget('recommend', key)))
    results = set(top_user_set) - set(recommend_list)

    return results


def save_recommentation2redis(date, user_set):
    hash_name = 'recommend'
    date = date.replace('-','')
    if user_set:
        r.hset(hash_name, date, json.dumps(list(user_set)))
    return 1

def read_black_user_list():
    results = set()
    f = open('./filter_uid_list', 'rb')
    reader = csv.reader(f)
    for line in reader:
        uid = line[0]
        results.add(uid)
    f.close()
    return results

def filter_rules(user_set):
    activity_filter = filter_activity(user_set)
    ip_filter = filter_ip(activity_filter)
    retweet_count_filter = filter_retweet_count(ip_filter)
    filter_results = filter_mention(retweet_count_filter)
    return filter_results

