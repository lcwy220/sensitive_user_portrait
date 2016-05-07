# -*- coding:utf-8 -*-
import sys
import redis
import IP
import time
import json
from elasticsearch import Elasticsearch

reload(sys)
sys.path.append('./../../')
from global_utils import R_ADMIN as r_sensitive
from global_utils import redis_cluster, redis_ip, redis_activity
from global_utils import ES_CLUSTER_FLOW2 as es_cluster
from global_utils import es_user_profile, es_flow_text,flow_text_index_name_pre, flow_text_index_type
from parameter import  RUN_TYPE, WORK_TYPE,ip_index_pre,MAX_VALUE,\
                       sen_ip_index_pre, act_index_pre, sen_act_index_pre, DAY, sensitive_score_dict
from time_utils import datetime2ts, ts2datetime,ts2date

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
        now_ts = time.time()
        now_date = ts2datetime(now_ts) # date: 2013-09-01
    else:
        now_date = "2013-09-08"
    ts = datetime2ts(now_date)

    start_ts = ts - 8*3600*24
    for i in range(1,8):
        ts = start_ts + i*3600*24
        date = ts2datetime(ts)
        print "date:", date
        uid_day_geo = {}
        sensitive_uid_day_geo = {}
        flow_index_name = flow_text_index_name_pre + str(date)
        # hashtag
        hashtag_results = redis_cluster.hmget('hashtag_'+str(ts), uid_list)
        sensitive_hashtag = redis_cluster.hmget('sensitive_hashtag_'+str(ts), uid_list)
        # sensitive_words
        sensitive_results = redis_cluster.hmget('sensitive_'+str(ts), uid_list)
        # ip
        if WORK_TYPE == 0:
            ip_index_name = ip_index_pre + str(date)
            sensitive_ip_index_name = sen_ip_index_pre + str(date)
            #activity_index_name = act_index_pre + str(date)
            #sensitive_activity_index_name = sen_act_index_pre + str(date)
            exist_bool = es_cluster.indices.exists(index=ip_index_name)
            sensitive_exist_bool = es_cluster.indices.exists(index=sensitive_ip_index_name)
            #activity_exist_bool = es_cluster.indices.exists(index=activity_index_name)
            #sensitive_activity_exist_bool = es_cluster.indices.exists(index=sensitive_activity_index_name)
            if exist_bool:
                ip_results = es_cluster.mget(index=ip_index_name, doc_type="ip", body={"ids":uid_list})["docs"]
            else:
                ip_results = [dict()]*lenth
            if sensitive_exist_bool:
                sensitive_ip_results = es_cluster.mget(index=sensitive_ip_index_name, doc_type="sensitive_ip", body={"ids":uid_list})["docs"]
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
            ip_results = redis_ip.hmget('ip_'+str(ts), uid_list)
            sensitive_ip_results = redis_ip.hmget('sensitive_ip_'+str(ts), uid_list)
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
            #print "sensitive_words:", iter_results[uid]["sensitive_words"]

            if hashtag_results[j]:
                hashtag_dict = json.loads(hashtag_results[j])
                for hashtag in hashtag_dict:
                    try:
                        iter_results[uid]['hashtag'][hashtag] += hashtag_dict[hashtag]
                    except:
                        iter_results[uid]['hashtag'][hashtag] = hashtag_dict[hashtag]
            #print "hashtag: ", iter_results[uid]['hashtag']

            if sensitive_hashtag[j]:
                sensitive_hashtag_dict = json.loads(sensitive_hashtag[j])
                for hashtag in sensitive_hashtag_dict:
                    try:
                        iter_results[uid]['sensitive_hashtag'][hashtag] += sensitive_hashtag_dict[hashtag]
                    except:
                        iter_results[uid]['sensitive_hashtag'][hashtag] = sensitive_hashtag_dict[hashtag]
            #print "sensitive_hashtag:", iter_results[uid]['sensitive_hashtag']

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
                #iter_results[uid]['ip'].append(ip_dict)
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
            #iter_results[uid]['ip'].append(ip_dict)
            iter_results[uid]['geo_track'].append(uid_day_geo[uid])
            #print "ip:", iter_results[uid]['ip'], iter_results[uid]['geo_track']

            if WORK_TYPE == 0:
                if sensitive_ip_results[j]:
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
                #iter_results[uid]['sensitive_ip'].append(sensitive_ip_dict)
                for geo, count in sensitive_geo_dict.iteritems():
                    try:
                        iter_results[uid]['sensitive_geo'][geo] += count
                    except:
                        iter_results[uid]['sensitive_geo'][geo] = count
                    try:
                        sensitive_uid_day_geo[uid][geo] += count
                    except:
                        sensitive_uid_day_geo[uid][geo] = count
            #iter_results[uid]['sensitive_ip'].append(sensitive_ip_dict)
            iter_results[uid]['sensitive_geo_track'].append(sensitive_uid_day_geo[uid])
            #print "sensitive_ip:", iter_results[uid]['sensitive_ip'], iter_results[uid]['sensitive_geo_track']

        # compute keywords
        flow_text_exist = es_flow_text.indices.exists(index=flow_index_name)
        if flow_text_exist:
             text_results = es_flow_text.search(index=flow_index_name, doc_type=flow_text_index_type,\
                    body={'query':{'filtered':{'filter':{'terms':{'uid': uid_list}}}}, 'size':MAX_VALUE},_source=False, fields=['uid', 'keywords_dict'])['hits']['hits']
        else:
            text_results = {}
        for item in text_results:
            uid = item['fields']['uid'][0]
            uid_keywords_dict = json.loads(item['fields']['keywords_dict'][0])
            for keywords in uid_keywords_dict:
                try:
                    iter_results[uid]['keywords'][keywords] += uid_keywords_dict[keywords]
                except:
                    iter_results[uid]['keywords'][keywords] = uid_keywords_dict[keywords]
        #print "keywords:", iter_results[uid]['keywords']

    for uid in uid_list:
        results[uid] = {}
        # hashtag
        hashtag_dict = iter_results[uid]['hashtag']
        results[uid]['hashtag_dict'] = json.dumps(hashtag_dict)
        results[uid]['hashtag_string'] = '&'.join(hashtag_dict.keys())
        # sensitive hashtag
        sensitive_hashtag_dict = iter_results[uid]['sensitive_hashtag']
        results[uid]['sensitive_hashtag_dict'] = json.dumps(sensitive_hashtag_dict)
        results[uid]['sensitive_hashtag_string'] = '&'.join(sensitive_hashtag_dict.keys())
        # sensitive_words
        sensitive_word_dict = iter_results[uid]['sensitive_words']
        results[uid]['sensitive_words_dict'] = json.dumps(sensitive_word_dict)
        results[uid]['sensitive_words_string'] = '&'.join(sensitive_word_dict.keys())
        sensitive_score = 0
        for k,v in sensitive_word_dict.iteritems():
            tmp = r_sensitive.hget('sensitive_words', k)
            if tmp:
                tmp_stage = json.loads(tmp)
                sensitive_score += sensitive_score_dict[str(tmp_stage[0])]*v
        results[uid]['sensitive'] = sensitive_score
        # geo
        geo_dict = iter_results[uid]['geo']
        geo_track_list = iter_results[uid]['geo_track']
        results[uid]['activity_geo_dict'] = json.dumps(geo_track_list)
        geo_dict_keys = geo_dict.keys()
        results[uid]['activity_geo'] = '&'.join(['&'.join(item.split('\t')) for item in geo_dict_keys])
        results[uid]['activity_geo_aggs'] = '&'.join([item.split('\t')[-1] for item in geo_dict_keys])
        sensitive_geo_dict = iter_results[uid]['sensitive_geo']
        sensitive_geo_track_list = iter_results[uid]['sensitive_geo_track']
        results[uid]['sensitive_activity_geo_dict'] = json.dumps(sensitive_geo_track_list)
        sensitive_geo_dict_keys = sensitive_geo_dict.keys()
        results[uid]['sensitive_activity_geo'] = '&'.join(['&'.join(item.split('\t')) for item in sensitive_geo_dict_keys])
        results[uid]['sensitive_activity_geo_aggs'] = '&'.join([item.split('\t')[-1] for item in sensitive_geo_dict_keys])

        keywords_dict = iter_results[uid]['keywords']
        keywords_top50 = sorted(keywords_dict.items(), key=lambda x:x[1], reverse=True)[:50]
        keywords_top50_string = '&'.join([keyword_item[0] for keyword_item in keywords_top50])
        results[uid]['keywords_dict'] = json.dumps(keywords_top50)
        results[uid]['keywords_string'] = keywords_top50_string

    return results





if __name__ == '__main__':
    test_uid = ['2112067715', '3356923604']
    result = get_flow_information(test_uid)
    print result
