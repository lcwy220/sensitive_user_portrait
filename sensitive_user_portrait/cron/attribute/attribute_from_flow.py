# -*- coding:utf-8 -*-
import sys
import redis
import IP
import time
import json
from elasticsearch import Elasticsearch

reload(sys)
sys.path.append('./../../')
from global_utils import R_CLUSTER_FLOW2 as r_cluster
from time_utils import datetime2ts, ts2datetime

def ip2geo(ip_dict):
    city_set = set()
    geo_dict = dict()
    for ip in ip_dict:
        try:
            city = IP.find(str(ip))
            if city:
                city.encode('utf-8')
            else:
                city=''
        except Exception, e:
            city = ''
        if city:
            len_city = len(city.split('\t'))
            if len_city == 4:
                city = '\t'.join(city.split('\t')[0:3])
            try:
                geo_city[city] += ip_dict[ip]
            except:
                geo_dict[city] = ip_dict[ip]
    return geo_dict

def extract_geo(result):
    geo_string = ''
    date_list = result.values()
    result_dict = {}
    result_list = []
    for item in date_list:
        result_dict.update(ip2geo(item))
    for geo in result_dict:
        result_list.append(geo.split('\t')[-1])
    geo_string = json.dumps(list(set(result_list)))
    return geo_string

def ip_to_geo(result):
    date_list = result.values()
    result_dict = {}
    for item in result:
        result_dict.update({item:ip2geo(result[item])})
    return result_dict

def extract_string(result):
    result_string = ''
    date_list = result.values()
    result_list = []
    for item in date_list:
        result_list.extend(item.keys())
    result_string = json.dumps(list(set(result_list)))
    return result_string

def get_flow_information(uid_list):
    result_dict = {}
    now_ts = time.time()
    now_date = ts2datetime(now_ts) # date: 2013-09-01
    ts = datetime2ts # 1234567890

    hashtag_results = {}
    geo_results = {}
    ts = datetime2ts('2013-09-08')
    user_hashtag_result = {}
    user_sensitive_hashtag = {}
    sensitive_words = {}
    user_ip_result = {}
    user_sensitive_ip = {}
    for i in range(1,8):
        ts = ts - 3600*24
        date = ts2datetime(ts).replace('-','')
        hashtag_results = r_cluster.hmget('hashtag_'+str(date), uid_list)
        sensitive_hashtag = r_cluster.hmget('sensitive_hashtag_'+str(date), uid_list)
        ip_results = r_cluster.hmget('ip_'+str(date), uid_list)
        sensitive_ip = r_cluster.hmget('sensitive_ip_'+str(date), uid_list)
        sensitive_results = r_cluster.hmget('sensitive_'+str(date), uid_list)

        for j in range(0, len(uid_list)):
            uid = uid_list[j]
            if sensitive_results[j]:
                sensitive_words_results = json.loads(sensitive_results[j])
                if sensitive_words.has_key(uid):
                    sensitive_words[uid].update({date: sensitive_words_results})
                else:
                    sensitive_words[uid] = {date: sensitive_words_results}
            if hashtag_results[j]:
                hashtag_dict = json.loads(hashtag_results[j])
                if user_hashtag_result.has_key(uid):
                    user_hashtag_result[uid].update({date: hashtag_dict})
                else:
                    user_hashtag_result[uid] = {date: hashtag_dict}
            if sensitive_hashtag[j]:
                sensitive_hashtag_dict = json.loads(sensitive_hashtag[j])
                if user_sensitive_hashtag.has_key(uid):
                    user_sensitive_hashtag[uid].update({date: sensitive_hashtag_dict})
                else:
                    user_sensitive_hashtag[uid] = {date: sensitive_hashtag_dict}
            if ip_results[j]:
                ip_dict = json.loads(ip_results[j])
                if user_ip_result.has_key(uid):
                    user_ip_result[uid].update({date: ip_dict})
                else:
                    user_ip_result[uid] = {date: ip_dict}
            if sensitive_ip[j]:
                sensitive_ip_result = json.loads(sensitive_ip[j])
                if user_sensitive_ip.has_key(uid):
                    user_sensitive_ip[uid].update({date: sensitive_ip_result})
                else:
                    user_sensitive_ip[uid] = {date: sensitive_ip_result}


    for uid in uid_list:
        hashtag_string = ''
        sensitive_hashtag_string = ''
        ip_string = ''
        sensitive_ip_string = ''
        hashtag_dict = {}
        sensitive_hashtag_dict = {}
        ip_dict = {}
        sensitive_ip_dict = {}
        sensitive_words_string = ''
        sensitive_words_dict = {}

        if sensitive_words.has_key(uid):
            sensitive_words_string = extract_string(sensitive_words[uid])
            sensitive_words_dict = json.dumps(sensitive_words[uid])
        if user_hashtag_result.has_key(uid):
            hashtag_string = extract_string(user_hashtag_result[uid])
            hashtag_dict = json.dumps(user_hashtag_result[uid])
        if user_sensitive_hashtag.has_key(uid):
            sensitive_hashtag_string = extract_string(user_sensitive_hashtag[uid])
            sensitive_hashtag_dict = json.dumps(user_sensitive_hashtag[uid])
        if user_ip_result.has_key(uid):
            ip_string = extract_geo(user_ip_result[uid])
            ip_dict = json.dumps(ip_to_geo(user_ip_result[uid]))
            ip_all = json.dumps(user_ip_result[uid])
        if user_sensitive_ip.has_key(uid):
            sensitive_ip_string = extract_geo(user_sensitive_ip[uid])
            sensitive_ip_dict = json.dumps(ip_to_geo(user_sensitive_ip[uid]))

        result_dict[uid] = {"hashtag_string": hashtag_string, "hashtag_dict": hashtag_dict, \
                            "sensitive_hashtag_string": sensitive_hashtag_string, "sensitive_hashtag_dict": sensitive_hashtag_dict, \
                            "geo_activity": ip_dict, "geo_string": ip_string, 'ip': ip_all, \
                             "sensitive_geo_activity": sensitive_ip_dict, "sensitive_geo_string":sensitive_ip_string, \
                             'sensitive_words_string': sensitive_words_string, 'sensitive_words_dict': sensitive_words_dict}
    return result_dict


if __name__ == '__main__':
    test_uid = ['3542550035']
    result = get_flow_information(test_uid)
