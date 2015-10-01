# -*- coding: UTF-8 -*-

import re
import sys
import time
import csv
import json
import redis
from elasticsearch import Elasticsearch
"""
reload(sys)
sys.path.append('./../')
from time_utils import ts2datetime, datetime2ts
from global_utils import R_DICT
from global_utils import R_CLUSTER_FLOW2 as r_cluster
from global_utils import es_sensitive_user_portrait as es
from global_utils import es_user_profile


"""
from sensitive_user_portrait.time_utils import ts2datetime, datetime2ts
from sensitive_user_portrait.global_utils import R_DICT
from sensitive_user_portrait.global_utils import R_CLUSTER_FLOW2 as r_cluster
from sensitive_user_portrait.global_utils import es_sensitive_user_portrait as es
from sensitive_user_portrait.global_utils import es_user_profile
from sensitive_user_portrait.recommentation.utils import get_user_trend, get_user_geo, get_user_hashtag

emotion_mark_dict = {'126': 'positive', '127':'negative', '128':'anxiety', '129':'angry'}
link_ratio_threshold = [0, 0.5, 1]
sensitive_text = 'sensitive_user_text'

def extract_uname(text):
    at_uname_list = []
    if isinstance(text, str):
        text = text.decode('utf-8', 'ignore')
    #text = text.split('//@')
    RE = re.compile(u'//@([a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+):', re.UNICODE)
    repost_chains = RE.findall(text)
    print repost_chains
    return repost_chains

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
                city = '\t'.join(city.split('\t')[0:3])
            try:
                geo_city[city] += ip_dict[ip]
            except:
                geo_dict[city] = ip_dict[ip]

    return geo_dict

def search_sensitive_text(uid):
    results = []
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "term":{
                        "uid": uid
                    }
                }
            }
        },
        "sort": {'timestamp': {'order': 'desc'}}
    }

    search_results = es.search(index='sensitive_user_text', doc_type='user', body=query_body)['hits']['hits']
    print search_results
    if search_results:
        results = search_results

    return results

def text_sentiment(text):
    text_list = [text]
    liwc_list = attr_liwc[text_list]
    emoticon_list = attr_emoticon

    return [liwc_list, emoticon_list]

def identify_uid_in(uid):
    result= []
    search_result = es.get(index='sensitive_user_portrait', doc_type="user", id=uid)['found']
    return search_result

def identify_uid_list_in(uid_list):
    in_set = set()
    search_result = es.mget(index='sensitive_user_portrait', doc_type="user", body={'ids':uid_list})['docs']
    for item in search_result:
        if item['found']:
            in_set.add(item['_id'])

    return in_set


# search users who has retweeted by the uid
def search_retweet(uid):
    stat_results = dict()
    results = dict()
    for db_num in R_DICT:
        r = R_DICT[db_num]
        ruid_results = r.hgetall('retweet_'+str(uid))
        #sensitive_ruid_results = r.hgetall('sensitive_retweet_'+str(uid)) # because of sensitive weibo
        if ruid_results:
            for ruid in ruid_results:
                if ruid != uid:
                    if stat_results.has_key(ruid):
                        stat_results[ruid] += ruid_results[ruid]
                    else:
                        stat_results[ruid] = ruid_results[ruid]

    if stat_results:
        sort_stat_results = sorted(stat_results.items(), key=lambda x:x[1], reverse=True)[:20]
    else:
        retune [None, 0]
    print 'sort_stat_results:', sort_stat_results
    uid_list = [item[0] for item in sort_stat_results]
    es_profile_results = es_user_profile.mget(index='weibo_user', doc_type='user', body={'ids':uid_list})['docs']
    es_portrait_results = es.mget(index='sensitive_user_portrait', doc_type='user', body={'ids':uid_list})['docs']
    result_list = []
    for i in range(len(es_profile_results)):
        item = es_profile_results[i]
        uid = item['_id']
        if item['found']:
            uname = item['_source']['nick_name']
        else:
            uname = u'unknown'

        portrait_item = es_portrait_results[i]
        if portrait_item['found']:
            in_status = 1
        else:
            in_status = 0

        result_list.append([uid,[uname, stat_results[uid], in_status]])

    return [result_list[:20], len(stat_results)]


def search_follower(uid):
    results = dict()
    stat_results = dict()
    for db_num in R_DICT:
        r = R_DICT[db_num]
        br_uid_results = r.hgetall('be_retweet_'+str(uid))
        if br_uid_results:
            for br_uid in br_uid_results:
                if br_uid != uid:
                    try:
                        stat_results[br_uid] += br_uid_results[br_uid]
                    except:
                        stat_results[br_uid] = br_uid_results[br_uid]
    if not stat_results:
        return [None, 0]
    try:
        sort_stat_results = sorted(stat_results.items(), key=lambda x:x[1], reverse=True)[:20]
    except:
        return [None, 0]

    uid_list = [item[0] for item in sort_stat_results]
    es_profile_results = es_user_profile.mget(index='weibo_user', doc_type='user', body={'ids':uid_list})['docs']
    es_portrait_results = es.mget(index='sensitive_user_portrait', doc_type='user', body={'ids':uid_list})['docs']

    result_list = []
    for i in range(len(es_profile_results)):
        item = es_profile_results[i]
        uid = item['_id']
        try:
            source = item['_source']
            uname = source['nick_name']
        except:
            uname = u'unknown'

        portrait_item = es_portrait_results[i]
        try:
            source = portrait_item['_source']
            in_status = 1
        except:
            in_status = 0
        result_list.append([uid,[uname, stat_results[uid], in_status]])
    return [result_list[:20], len(stat_results)]


def search_mention(uid):
    date = ts2datetime(time.time()).replace('-','')
    stat_results = dict()
    results = dict()
    test_ts = time.time()
    test_ts = datetime2ts('2013-09-07')
    for i in range(0,7):
        ts = test_ts -i*24*3600
        date = ts2datetime(ts).replace('-', '')
        at_temp = r_cluster.hget('at_' + str(date), str(uid))
        if not at_temp:
            continue
        else:
            result_dict = json.loads(result_string)
        for at_uid in result_dict:
            if stat_results.has_key(at_uid):
                stat_results[uid] += result_dict[uid]
            else:
                stat_results[uid] = result_dict[uid]
    if not stat_results:
        return [None, 0]

    in_status = identify_uid_list_in(result_dict.keys())
    for at_uid in result_dict:
        if at_uid in in_status:
            results[at_uid] = [result_dict[at_uid], '1']
        else:
            results[at_uid] = [result_dict[at_uid], '0']

    sorted_results = sorted(results.items(), key=lambda x:x[1][0], reverse=True)
    return [sorted_results[0:20], len(results)]


# show user's attributions saved in sensitive_user_portrait
def search_attribute_portrait(uid):
    results = {}
    index_name = "sensitive_user_portrait"
    index_type = "user"

    try:
        search_result = es.get(index=index_name, doc_type=index_type, id=uid)
    except:
        return None
    results = search_result['_source']

    keyword_list = []
    if results['keywords']:
        keywords_dict = json.loads(results['keywords'])
        sort_word_list = sorted(keywords_dict.items(), key=lambda x:x[1], reverse=True)
        results['keywords'] = sort_word_list
    else:
        results['keywords'] = []

    geo_top = []
    temp_geo = {}
    '''
    if results['geo_activity']:
        geo_dict = json.loads(results['geo_activity'])
        geo_list = geo_dict.values()
        for item in geo_list:
            for iter_key in item.keys():
                if temp_geo.has_key(iter_key):
                    temp_geo[iter_key] += item[iter_key]
                else:
                    temp_geo[iter_key] = item[iter_key]
        sort_geo_dict = sorted(temp_geo.items(), key=lambda x:x[1], reverse=True)
        results['activity_geo'] = sort_geo_dict
    else:
        results['activity_geo'] = []
    '''
    geo_dict = get_user_geo(uid)[0]
    results['activity_geo'] = geo_dict

    hashtag_dict = get_user_hashtag(uid)[0]
    results['hashtag'] = hashtag_dict

    emotion_result = {}
    emotion_conclusion_dict = {}
    if results['emotion_words']:
        emotion_words_dict = json.loads(results['emotion_words'])
        for word_type in emotion_mark_dict:
            try:
                word_dict = emotion_words_dict[word_type]
                if word_type=='126' or word_type=='127':
                    emotion_conclusion_dict[word_type] = word_dict
                sort_word_dict = sorted(word_dict.items(), key=lambda x:x[1], reverse=True)
                word_list = sort_word_dict[:5]
            except:
                results['emotion_words'] = emotion_result
            emotion_result[emotion_mark_dict[word_type]] = word_list
    results['emotion_words'] = emotion_result

    # topic
    if results['topic']:
        topic_dict = json.loads(results['topic'])
        sort_topic_dict = sorted(topic_dict.items(), key=lambda x:x[1], reverse=True)
        results['topic'] = sort_topic_dict[:5]
    else:
        results['topic'] = []

    # domain
    if results['domain']:
        domain_string = results['domain']
        domain_list = domain_string.split('_')
        results['domain'] = domain_list
    else:
        results['domain'] = []

    # emoticon
    if results['emotion']:
        emotion_dict = json.loads(results['emotion'])
        sort_emotion_dict = sorted(emotion_dict.items(), key=lambda x:x[1], reverse=True)
        results['emotion'] = sort_emotion_dict[:5]
    else:
        results['emotion'] = []

    # on_line pattern
    if results['online_pattern']:
        online_pattern_dict = json.loads(results['online_pattern'])
        sort_online_pattern_dict = sorted(online_pattern_dict.items(), key=lambda x:x[1], reverse=True)
        results['online_pattern'] = sort_online_pattern_dict[:5]
    else:
        results['online_pattern'] = []

    # psycho_status
    if results['psycho_status']:
        psycho_status_dict = json.loads(results['psycho_status'])
        sort_psycho_status_dict = sorted(psycho_status_dict.items(), key=lambda x:x[1], reverse=True)
        results['psycho_status'] = sort_psycho_status_dict[:5]
    else:
        results['psycho_status'] = []

    #psycho_feature
    if results['psycho_feature']:
        psycho_feature_list = results['psycho_feature'].split('_')
        results['psycho_feature'] = psycho_feature_list
    else:
        results['psycho_feature'] = []

    # self_state
    try:
        profile_result = es_user_profile.get(index='weibo_user', doc_type='user', id=uid)
        self_state = profile_result['_source'].get('description', '')
        results['description'] = self_state
    except:
        results['description'] = ''
    if results['importance']:
        query_body = {
            'query':{
                'range':{
                    'importance':{
                        'from':results['importance'],
                        'to': 100000
                    }
                }
            }
        }
        importance_rank = es.count(index='sensitive_user_portrait', doc_type='user', body=query_body)
        if importance_rank['_shards']['successful'] != 0:
            results['importance_rank'] = importance_rank['count']
        else:
            print 'es_importance_rank error'
            results['importance_rank'] = 0
    else:
        results['importance_rank'] = 0

    
    if results['activeness']:
        query_body = {
            'query':{
                'range':{
                    'activeness':{
                        'from':results['activeness'],
                        'to': 100000
                    }
                }
            }
        }
        activeness_rank = es.count(index='sensitive_user_portrait', doc_type='user', body=query_body)
        if activeness_rank['_shards']['successful'] != 0:
            results['activeness_rank'] = activeness_rank['count']
        else:
            print 'es_activeness_rank error'
            results['activeness_rank'] = 0
    else:
        results['activeness_rank'] = 0


    if results['influence']:
        query_body = {
            'query':{
                'range':{
                    'influence':{
                        'from':results['influence'],
                        'to': 100000
                    }
                }
            }
        }
        influence_rank = es.count(index='sensitive_user_portrait', doc_type='user', body=query_body)
        if influence_rank['_shards']['successful'] != 0:
            results['influence_rank'] = influence_rank['count']
        else:
            print 'es_influence_rank error'
            results['influence_rank'] = 0
    else:
        results['influence_rank'] = 0

    query_body = {
        'query':{
            "match_all":{}
        }
    }
    all_count = es.count(index='sensitive_user_portrait', doc_type='user', body=query_body)['count']

    # link
    link_ratio = results['link']

    weibo_trend = get_user_trend(uid)
    results['weibo_trend'] = weibo_trend[0]


    return results


def search_portrait(condition_num, query, sort, size):
    user_result = []
    index_name = 'sensitive_user_portrait'
    index_type = 'user'
    if condition_num > 0:
        result = es.search(index=index_name, doc_type=index_type, \
            body={'query':{'bool':{'must':query}}, 'sort':sort, 'size':size})['hits']['hits']

    else:
        result = es.search(index=index_name, doc_type=index_type, \
                    body={'query':{'match_all':{}}, 'sort':[{sort:{"order":"desc"}}], 'size':size})['hits']['hits']
    if result:
        for item in result:
            user_dict = item['_source']
            score = item['_score']
            if not user_dict['uname']:
                user_dict['uname'] = 'unknown'
            if not user_dict['location']:
                user_dict['location'] = 'unknown'

            user_result.append([user_dict['uid'], user_dict['uname'], user_dict['location'], user_dict['activeness'], user_dict['importance'], user_dict['influence'], score])

    return user_result


def sensitive_attribute(uid):
    results = {}

    # sensitive weibo number statistics
    date = ts2datetime(time.time()-24*3600).replace('-', '')
    date = '20130907' # test
    influence_results = []
    try:
        influence_results = es.get(index=date, doc_type='bci', id=uid)['_source']
        sensitive_origin_weibo_number = influence_results.get('s_origin_weibo_number', 0)
        sensitive_retweeted_weibo_number = influence_results.get('s_retweeted_weibo_number', 0)
        sensitive_comment_weibo_number = influence_results.get('s_comment_weibo_number', 0)
        origin_weibo_number = influence_results.get('origin_weibo_number', 0)
        retweeted_weibo_number = influence_results.get('retweeted_weibo_number', 0)
        comment_weibo_number = influence_results.get('comment_weibo_number', 0)
        if sensitive_origin_weibo_number or origin_weibo_number:
            results['proportion_sensitive_origin_weibo'] = sensitive_origin_weibo_number/(sensitive_origin_weibo_number+origin_weibo_number)
        else:
            results['proportion_sensitive_origin_weibo'] = 0
        if sensitive_retweeted_weibo_number or retweeted_weibo_number:
            results['proportion_sensitive_retweeted_weibo'] = sensitive_retweeted_weibo_number/(sensitive_retweeted_weibo_number+retweeted_weibo_number)
        else:
            results['proportion_sensitive_retweeted_weibo'] = 0
        if sensitive_comment_weibo_number or comment_weibo_number:
            results['proportion_sensitive_comment_weibo'] = sensitive_comment_weibo_number/(sensitive_comment_weibo_number+comment_weibo_number)
        else:
            results['proportion_sensitive_comment_weibo'] = 0
        results['sensitive_origin_weibo'] = sensitive_origin_weibo_number
        results['sensitive_retweeted_weibo'] = sensitive_retweeted_weibo_number
        results['sensitive_comment_weibo'] = sensitive_comment_weibo_number
    except:
        results['proportion_sensitive_origin_weibo'] = 0
        results['proportion_sensitive_retweeted_weibo'] = 0
        results['proportion_sensitive_comment_weibo'] = 0
        results['sensitive_origin_weibo'] = 0
        results['sensitive_retweeted_weibo'] = 0
        results['sensitive_comment_weibo'] = 0

    sensitive_text = search_sensitive_text(uid)
    text_detail = []
    if sensitive_text:
        for item in sensitive_text:
            text_
            item = item['_source']
            text = item['text']
            


if __name__ == '__main__':
    print get_user_trend('1744768687')
