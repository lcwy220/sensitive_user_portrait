# -*- coding:utf-8 -*-
import sys
import redis
import IP
import time
import json
from elasticsearch import Elasticsearch

reload(sys)
sys.path.append('./../../')
from global_utils import R_CLUSTER_FLOW2 as r_cluster #ip activity es
from global_utils import redis_cluster, redis_ip, redis_activity
from global_utils import es_user_profile, 
from time_utils import datetime2ts, ts2datetime, RUN_TYPE, WORK_TYPE,ip_index_pre,\
                       sen_ip_index_pre, act_index_pre, sen_act_index_pre, DAY

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
                city = '&'.join(city.split('\t')[0:3])
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
    geo_string = '&'.join(list(set(result_list)))
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
    result_string = '&'.join(list(set(result_list)))
    return result_string

# hashtag activity_geo ip sensitive_words
def get_flow_information(uid_list):
    # 前七天的数据, 不能用于每天更新
    lenth = len(uid_list)
    results = {}
    iter_results = {}
    result_dict = {}
    if RUN_TYPE:
        now_ts = time.time()-3600*24
        now_date = ts2datetime(now_ts) # date: 2013-09-01
    else:
        now_date = "2013-09-08"
    ts = datetime2ts(now_date)

    hashtag_results = {}
    user_sensitive_hashtag = {}
    geo_results = {}
    sensitive_geo_results = {}
    user_hashtag_result = {}
    sensitive_words = {}
    user_ip_result = {}
    user_sensitive_ip = {}
    activity_results = {}
    sensitive_activity_results = {}
    for i in range(1,8):
        ts = ts - 3600*24
        date = ts2datetime(ts)
        # hashtag
        hashtag_results = redis_cluster.hmget('hashtag_'+str(date), uid_list)
        sensitive_hashtag = redis_cluster.hmget('sensitive_hashtag_'+str(date), uid_list)
        # sensitive_words
        sensitive_results = redis_cluster.hmget('sensitive_'+str(date), uid_list)
        # ip
        if WORK_TYPE == 0:
            ip_index_name = ip_index_pre + str(date)
            sensitive_ip_index_name = sen_ip_index_pre + str(date)
            activity_index_name = act_index_pre + str(date)
            sensitive_activity_index_name = sen_act_index_pre + str(date)
            exist_bool = es_cluster.indices.exists(index=ip_index_name)
            sensitive_exist_bool = es_cluster.indices.exists(index=sensitive_ip_index_name)
            #activity_exist_bool = es_cluster.indices.exists(index=activity_index_name)
            #sensitive_activity_exist_bool = es_cluster.indices.exists(index=sensitive_activity_index_name)
            if exist_bool:
                ip_results = es_cluster.mget(index=index_name, doc_type="ip", body={"ids":uid_list})["docs"]
            else:
                ip_results = [dict()]*lenth
            if sensitive_exist_bool:
                sensitive_ip_results = es_cluster.mget(index=sensitive_index_name, doc_type="sensitive_ip", body={"ids":uid_list})["docs"]
            else:
                sensitive_ip_results = [dict()]*lenth
            """
            if activity_exist_bool:
                activity_results = es_cluster.mget(index=activity_index_name, doc_type="activity", body={"ids":uid_list})["docs"]
            else:
                activity_results = [dict()]*lenth
            if sensitive_activity_exist_bool:
                sensitive_activity_results = es_cluster.mget(index=sensitive_activity_index_name, doc_type="sensitive_activity", body={"ids":uid_list})["docs"]
            else:
                sensitive_activity_results = [dict()]*lenth
            """
        else:
            ip_results = redis_ip.hmget('ip_'+str(date), uid_list)
            sensitive_ip_results = redis_ip.hmget('sensitive_ip_'+str(date), uid_list)
            #activity_results = redis_activity.hmget('activity_'+str(date), uid_list)
            #sensitive_activity_results = redis_activity.hmget('sensitive_activity_'+str(date), uid_list)

        for j in range(0, len(uid_list)):
            uid = uid_list[j]
            if uid not in iter_results:
                iter_results[uid] = {'hashtag':{}, 'sensitive_hashtag':{}, 'geo':{}, "sensitive_geo":{},'geo_track':[],'keywords':{}, \
                        'sensitive_words':{}, "sensitive_geo_track":[],'ip': [], 'sensitive_ip':[]}
            # sensitive words
            if sensitive_results[j]:
                sensitive_words_results = json.loads(sensitive_results[j])
                for sensitive_word in sensitive_words_results:
                    try:
                        iter_results[uid]["sensitive_words"][sensitive_word] += sensitive_words_results[sensitive_word]
                    except:
                        iter_results[uid]["sensitive_words"][sensitive_word] = sensitive_words_results[sensitive_word]

            if hashtag_results[j]:
                hashtag_dict = json.loads(hashtag_results[j])
                for hashtag in hashtag_dict:
                    try:
                        iter_results[uid]['hashtag'][hashtag] += hashtag_dict[hashtag]
                    except:
                        iter_results[uid]['hashtag'][hashtag] = hashtag_dict[hashtag]

            if sensitive_hashtag[j]:
                sensitive_hashtag_dict = json.loads(sensitive_hashtag[j])
                for hashtag in sensitive_hashtag_dict:
                    try:
                        iter_results[uid]['sensitive_hashtag'] += sensitive_hashtag_dict[hashtag]
                    except:
                        iter_results[uid]['sensitive_hashtag'] = sensitive_hashtag_dict[hashtag]

            uid_day_geo[uid] = {}
            sensitive_uid_day_geo[uid] = {}
            if WORK_TYPE == 0:# es
                if ip_results[j]:
                    if ip_results[j]['found']:
                        detail_item = ip_results[j]['_source']
                        ip_dict = json.loads(detail_item['ip_dict'])
                    else:
                        ip_dict = {}
                else:
                    ip_dict = {}
            else:
                if ip_results[j]:
                    ip_dict = json.loads(ip_results[j])
                else:
                    ip_dict = {}
            if ip_dict:
                iter_results[uid]['ip'].append(ip_dict)
                geo_dict = ip2geo(ip_dict)
                for geo, count in geo_dict.iteritems():
                    try:
                        iter_results[uid]['geo'][geo] += count
                    except:
                        iter_results[uid]['geo'][geo] = count
                    try:
                        uid_day_geo[uid][geo] += count
                    except:
                        uid_day_geo[uid][geo] = count
            else:
                iter_results[uid]['ip'].append({})
                iter_results[uid]['geo_track'].append(uid_day_geo[uid])

            if WORK_TYPE == 0:
                if sensitive_ip[j]:
                    if sensitive_ip_results[j]['found']:
                        detail_item = sensitive_ip_results[j]['_source']
                        sensitive_ip_dict = json.loads(detail_item['sensitive_ip_dict'])
                    else:
                        sensitive_ip_dict = dict()
                else:
                    sensitive_ip_dict = dict()
            else:
                if sensitive_ip_results[j]:
                    sensitive_ip_dict = json.loads(sensitive_ip_results[j])
                else:
                    sensitive_ip_dict = dict()
            if sensitive_ip_dict:
                sensitive_geo_dict = ip2geo(sensitive_ip_dict)
                iter_results[uid]['sensitive_ip'].append(sensitive_ip_dict)
                for geo, count in sensitive_ip_dict.iteritems():
                    try:
                        iter_results[uid]['sensitive_geo'][geo] += count
                    except:
                        iter_results[uid]['sensitive_geo'][geo] = count
                    try:
                        sensitive_uid_day_geo[uid][geo] += count
                    except:
                        sensitive_uid_day_geo[uid][geo] = count
            else:
                iter_results[uid]['sensitive_ip'].append({})
                iter_results[uid]['sensitive_geo_track'].append(sensitive_uid_day_geo[uid])


    for uid in uid_list:
        hashtag_string = ''
        sensitive_hashtag_string = ''
        ip_string = ''
        ip_all = ""
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
