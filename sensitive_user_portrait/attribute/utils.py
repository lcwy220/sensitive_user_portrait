# -*- coding: UTF-8 -*-

import re
import sys
import time
import csv
import json
import math
import redis
from elasticsearch import Elasticsearch
from description import active_geo_description, active_time_description, hashtag_description
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
from sensitive_user_portrait.global_utils import R_RECOMMENTATION as r
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

def sort_sensitive_words(words_list):
    sensitive_words_list = []
    for item in words_list:
        temp = []
        temp.extend(item)
        word = (item[0]).encode('utf-8', 'ignore')
        r_word = r.hget('sensitive_words', word)
        if r_word:
            temp.extend(json.loads(r_word))
        else:
            temp.extend([1,'politics'])
        sensitive_words_list.append(temp)
    return sensitive_words_list

def search_full_text(uid, date):
    result = []
    ts = datetime2ts(date)
    next_ts = ts + 24*3600
    query_body = {
        "query": {
            "filtered":{
                "filter":{
                    "bool": {
                        "must": [
                            {"term": {"uid": uid}},
                            {"range": {
                                "timestamp":{
                                     "gte": ts,
                                     "lt": next_ts
                                }
                            }}
                        ]
                    }
                }
            }
        },
        "size": 200
    }

    search_results = es.search(index='sensitive_user_text', doc_type="user", body=query_body)['hits']['hits']
    for item in search_results:
        detail = []
        source = item['_source']
        detail.append(source['sensitive'])
        detail.append(source['message_type'])
        ts =source['timestamp']
        re_time = time.strftime('%H:%M:%S', time.localtime(float(ts)))
        detail.append(re_time)
        geo_string = source['geo']
        geo_list = geo_string.split('/t')
        if len(geo_list) >= 3:
            geo = '/t'.join(geo_list[-2:])
        else:
            geo = geo_string
        detail.append(geo)
        detail.append(source['text'])
        date = date.replace('-', '')
        mid = source['mid']
        try:
            weibo_bci = es.get(index=date, doc_type='bci', id=uid)['_source']
        except:
            weibo_bci = {}
        retweeted_number = 0
        comment_number = 0
        if source['sensitive']:
            print source
            if int(source['message_type']) == 1:
                if weibo_bci:
                    print weibo_bci['s_origin_weibo_retweeted_detail']
                    retweeted_number = weibo_bci.get('s_origin_weibo_retweeted_detail', {}).get(mid, 0)
                    comment_number = weibo_bci.get('s_origin_weibo_comment_detail', {}).get(mid, 0)
            elif int(source['message_type']) == 2:
                if weibo_bci:
                    retweeted_number = weibo_bci.get('s_retweeted_weibo_retweeted_detail', {}).get(mid, 0)
                    comment_number = weibo_bci.get('s_retweeted_weibo_comment_detail', {}).get(mid, 0)
            else:
                pass
        else:
            if int(source['message_type']) == 1:
                if weibo_bci:
                    retweeted_number = weibo_bci.get('origin_weibo_retweeted_detail', {}).get(mid, 0)
                    comment_number = weibo_bci.get('origin_weibo_comment_detail', {}).get(mid, 0)
            elif int(source['message_type']) == 2:
                if weibo_bci:
                    retweeted_number = weibo_bci.get('retweeted_weibo_retweeted_detail', {}).get(mid, 0)
                    comment_number = weibo_bci.get('retweeted_weibo_comment_detail', {}).get(mid, 0)
            else:
                pass
        detail.append(retweeted_number)
        detail.append(comment_number)
        result.append(detail)

    return result

def search_sensitive_text(uid, stype=0, sort_type="timestamp"):
    results = []
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"term": {"uid": uid}},
                            {"term": {"sensitive": 1}}
                        ]
                    }
                }
            }
        },
        "sort": {'timestamp': {'order': 'desc'}}
    }
    
    query_body['sort'] = {sort_type: {'order': 'desc'}}

    if stype == 0:
        search_results = es.search(index='sensitive_user_text', doc_type='user', body=query_body)['hits']['hits']
    elif int(stype) == 1:
        query_body["query"]["filtered"]["filter"]["bool"]["must"].append({"term": {"message_type": 1}})
    elif int(stype) == 2:
        query_body["query"]["filtered"]["filter"]["bool"]["must"].append({"term": {"message_type": 2}})
    else:
        pass

    if search_results:
        results = search_results
    return results

def text_sentiment(text):
    text_list = [text]
    liwc_list = attr_liwc(text_list)

    return liwc_list

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

def user_type(uid):
    try:
        result = es.get(index='sensitive_user_portrait', doc_type="user", id=uid)['_source']['type']
    except:
        result = ''

    return result


# search users who has retweeted by the uid
def search_retweet(uid, sensitive):
    stat_results = dict()

# search users who has retweeted by the uid
def search_retweet(uid, sensitive):
    stat_results = dict()
    results = dict()
    for db_num in R_DICT:
        r = R_DICT[db_num]
        if not sensitive:
            ruid_results = r.hgetall('retweet_'+str(uid))
        else:
            ruid_results = r.hgetall('sensitive_retweet_'+str(uid)) # because of sensitive weibo
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
        return [None, 0]
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


def search_follower(uid, sensitive):
    results = dict()
    stat_results = dict()
    for db_num in R_DICT:
        r = R_DICT[db_num]
        if sensitive:
            br_uid_results = r.hgetall('sensitive_be_retweet_'+str(uid))
        else:
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


def search_mention(uid, sensitive):
    date = ts2datetime(time.time()).replace('-','')
    stat_results = dict()
    results = dict()
    test_ts = time.time()
    test_ts = datetime2ts('2013-09-07')
    for i in range(0,7):
        ts = test_ts -i*24*3600
        date = ts2datetime(ts).replace('-', '')
        if not sensitive:
            at_temp = r_cluster.hget('at_' + str(date), str(uid))
        else:
            at_temp = r_cluster.hget('sensitive_at_' + str(date), str(uid))
        if not at_temp:
            continue
        else:
            result_dict = json.loads(at_temp)
        for at_uid in result_dict:
            if stat_results.has_key(at_uid):
                stat_results[uid] += result_dict[at_uid]
            else:
                stat_results[uid] = result_dict[at_uid]
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

def user_sentiment_trend(uid):
    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "term": {"uid": uid}
                }
            }
        }
    }
    search_results = es.search(index='sensitive_user_text', doc_type='user', body=query_body)['hits']['hits']
    sentiment_dict = dict()
    sentiment_results = dict()
    for item in search_results:
        datetime = ts2datetime(float(item['_source']['timestamp'])).replace('-', '')
        try:
            sentiment_dict[datetime].append(json.loads(item['_source']['sentiment']))
        except:
            sentiment_dict[datetime] = [json.loads(item['_source']['sentiment'])]
    total_positive = 0
    total_negetive = 0
    total_neutral = 0
    for datetime, sentiment_detail in sentiment_dict.items():
        positive_count = 0
        negetive_count = 0
        neutral_count = 0
        sentiment_results[datetime] = {}
        for item in sentiment_detail:
            if not item:
                try:
                    neutral_count += 1
                except:
                    neutral_count  = 1
                total_neutral += 1
                continue
            positive_dict = item.get('126', {})
            positive = sum(positive_dict.values())
            positive_count += positive
            negetive = sum(item.get('127', {}).values()) + sum(item.get('128', {}).values()) + sum(item.get('129', {}).values())
            negetive_count += negetive
            if positive > negetive:
                total_positive += 1
            elif positive < negetive:
                total_negetive += 1
            else:
                total_neutral += 1
        sentiment_results[datetime]['neutral'] = neutral_count
        sentiment_results[datetime]['positive'] = positive_count
        sentiment_results[datetime]['negetive'] = negetive_count
    return [[total_positive, total_neutral, total_negetive], sentiment_results]

def sort_sensitive_text(uid):
    sensitive_text = search_sensitive_text(uid)
    text_all = []
    if sensitive_text:
        for item in sensitive_text:
            text_detail = []
            item = item['_source']
            if not item['sensitive']:
                continue
            text = item['text']
            sentiment_dict = json.loads(item['sentiment'])
            if not sentiment_dict:
                sentiment = 0
            else:
                positive = len(sentiment_dict.get('126', {}))
                negetive = len(sentiment_dict.get('127', {})) + len(sentiment_dict.get('128', {})) + len(sentiment_dict.get('129', {}))
                if positive > negetive:
                    sentiment = 1
                elif positive < negetive:
                    sentiment = -1
                else:
                    sentiment = 0
            ts =item['timestamp']
            uid = item['uid']
            mid = item['mid']
            message_type = item.get('message_type', 0)
            date = ts2datetime(float(ts)).replace('-', '')
            try:
                bci_result = es.get(index=date, doc_type='bci', id=uid)['_source']
                if int(message_type) == 1:
                    retweeted_number = bci_result['s_origin_weibo_retweeted_detail'].get(mid)
                    comment_number = bci_result['s_origin_weibo_comment_detail'].get(mid)
                elif int(message_type) == 2:
                    retweeted_number = bci_result['s_retweeted_weibo_retweeted_detail'].get(mid)
                    comment_number = bci_result['s_retweeted_weibo_comment_detail'].get(mid)
                else:
                    retweeted_number = 0
                    comment_number = 0
            except:
                retweeted_number = 0
                comment_number = 0
            single_sw = item.get('sensitive_words', {})
            if single_sw:
                sw = json.loads(single_sw).keys()
            else:
                # print item
                sw = []
            geo = item['geo']
            retweeted_link = extract_uname(text)
            text_detail.extend([ts, geo, text, sw, retweeted_link, sentiment, message_type, retweeted_number, comment_number])
            text_all.append(text_detail)
    return text_all

# show user's attributions saved in sensitive_user_portrait
def search_attribute_portrait(uid):
    return_results = {}
    index_name = "sensitive_user_portrait"
    index_type = "user"

    try:
        search_result = es.get(index=index_name, doc_type=index_type, id=uid)
    except:
        return None
    results = search_result['_source']
    #return_results = results
    user_sensitive = user_type(uid)
    if user_sensitive:
        #return_results.update(sensitive_attribute(uid))
        return_results['user_type'] = 1
        return_results['sensitive'] = 1
    else:
        return_results['user_type'] = 0
        return_results['sensitive'] = 0

    return_results['photo_url'] = results['photo_url']
    return_results['uid'] = results['uid']
    return_results['uname'] = results['uname']
    return_results['location'] = results['location']
    return_results['fansnum'] = results['fansnum']
    return_results['friendsnum'] = results['friendsnum']
    return_results['gender'] = results['gender']

    keyword_list = []
    if results['keywords']:
        keywords_dict = json.loads(results['keywords'])
        sort_word_list = sorted(keywords_dict.items(), key=lambda x:x[1], reverse=True)
        return_results['keywords'] = sort_word_list
    else:
        return_results['keywords'] = []

    if return_results['sensitive']:
        sentiment_trend = user_sentiment_trend(uid)
        emotion_number = sentiment_trend[0]
        return_results['negetive_index'] = float(emotion_number[2])/(emotion_number[2]+emotion_number[1]+emotion_number[0])
        return_results['negetive_influence'] = float(emotion_number[1])/(emotion_number[2]+emotion_number[1]+emotion_number[0])
        sentiment_dict = sentiment_trend[1]
        datetime = ts2datetime(time.time()).replace('-', '')
        return_sentiment = dict()
        return_sentiment['positive'] = []
        return_sentiment['neutral'] = []
        return_sentiment['negetive'] = []
        ts = time.time()
        ts = datetime2ts('2013-09-08') - 8*24*3600
        for i in range(1,8):
            ts = ts + 24*3600
            date = ts2datetime(ts).replace('-', '')
            temp = sentiment_dict.get(date, {})
            return_sentiment['positive'].append(temp.get('positive', 0))
            return_sentiment['negetive'].append(temp.get('negetive', 0))
            return_sentiment['neutral'].append(temp.get('neutral', 0))
        return_results['sentiment_trend'] = return_sentiment

    return_results['retweet'] = search_retweet(uid, 0)
    return_results['follow'] = search_follower(uid, 0)
    return_results['at'] = search_mention(uid, 0)

    if results['ip'] and results['geo_activity']:
        ip_dict = json.loads(results['ip'])
        geo_dict = json.loads(results['geo_activity'])
        geo_description = active_geo_description(ip_dict, geo_dict)
        return_results['geo_description'] = geo_description
    else:
        return_results['geo_description'] = ''

    geo_top = []
    temp_geo = {}

    if results['geo_activity']:
        geo_dict = json.loads(results['geo_activity'])
        if len(geo_dict) < 7:
            ts = time.time()
            ts = datetime2ts('2013-09-08') - 8*24*3600
            for i in range(7):
                ts = ts + 24*3600
                date = ts2datetime(ts).replace('-', '')
                if geo_dict.has_key(date):
                    pass
                else:
                    geo_dict[date] = {}
        activity_geo_list = sorted(geo_dict.items(), key=lambda x:x[0], reverse=False)
        geo_list = geo_dict.values()
        for k,v in activity_geo_list:
            sort_v = sorted(v.items(), key=lambda x:x[1], reverse=True)
            top_geo = [item[0] for item in sort_v]
            geo_top.append([k, top_geo[0:2]])
            for iter_key in v.keys():
                if temp_geo.has_key(iter_key):
                    temp_geo[iter_key] += v[iter_key]
                else:
                    temp_geo[iter_key] = v[iter_key]
        sort_geo_dict = sorted(temp_geo.items(), key=lambda x:x[1], reverse=True)
        return_results['top_activity_geo'] = sort_geo_dict
        return_results['activity_geo_distribute'] = geo_top
    else:
        return_results['top_activity_geo'] = []
        return_results['activity_geo_distribute'] = geo_top

    hashtag_dict = get_user_hashtag(uid)[0]
    return_results['hashtag'] = hashtag_dict

    '''
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
    return_results['emotion_words'] = emotion_result
    '''

    # topic
    if results['topic']:
        topic_dict = json.loads(results['topic'])
        sort_topic_dict = sorted(topic_dict.items(), key=lambda x:x[1], reverse=True)
        return_results['topic'] = sort_topic_dict[:5]
    else:
        return_results['topic'] = []

    # domain
    if results['domain']:
        domain_string = results['domain']
        domain_list = domain_string.split('_')
        return_results['domain'] = domain_list
    else:
        return_results['domain'] = []
    '''
    # emoticon
    if results['emotion']:
        emotion_dict = json.loads(results['emotion'])
        sort_emotion_dict = sorted(emotion_dict.items(), key=lambda x:x[1], reverse=True)
        return_results['emotion'] = sort_emotion_dict[:5]
    else:
        return_results['emotion'] = []
    '''

    # on_line pattern
    if results['online_pattern']:
        online_pattern_dict = json.loads(results['online_pattern'])
        sort_online_pattern_dict = sorted(online_pattern_dict.items(), key=lambda x:x[1], reverse=True)
        return_results['online_pattern'] = sort_online_pattern_dict[:5]
    else:
        return_results['online_pattern'] = []


    # psycho_status
    if results['psycho_status']:
        psycho_status_dict = json.loads(results['psycho_status'])
        sort_psycho_status_dict = sorted(psycho_status_dict.items(), key=lambda x:x[1], reverse=True)
        return_results['psycho_status'] = sort_psycho_status_dict[:5]
    else:
        return_results['psycho_status'] = []

    '''
    #psycho_feature
    if results['psycho_feature']:
        psycho_feature_list = results['psycho_feature'].split('_')
        return_results['psycho_feature'] = psycho_feature_list
    else:
        return_results['psycho_feature'] = []
    '''

    # self_state
    try:
        profile_result = es_user_profile.get(index='weibo_user', doc_type='user', id=uid)
        self_state = profile_result['_source'].get('description', '')
        return_results['description'] = self_state
    except:
        return_results['description'] = ''
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
            return_results['importance_rank'] = importance_rank['count']
        else:
            return_results['importance_rank'] = 0
    else:
        return_results['importance_rank'] = 0
    return_results['importance'] = results['importance']

    if results['activeness']:
        query_body = {
            'query':{
                'range':{
                    'activeness':{
                        'from':results['activeness'],
                        'to': 10000
                    }
                }
            }
        }
        activeness_rank = es.count(index='sensitive_user_portrait', doc_type='user', body=query_body)
        print activeness_rank
        if activeness_rank['_shards']['successful'] != 0:
            return_results['activeness_rank'] = activeness_rank['count']
        else:
            return_results['activeness_rank'] = 0
    else:
        return_results['activeness_rank'] = 0
    return_results['activeness'] = results['activeness']

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
            return_results['influence_rank'] = influence_rank['count']
        else:
            return_results['influence_rank'] = 0
    else:
        return_results['influence_rank'] = 0
    return_results['influence'] = results['influence']


    if results['sensitive']:
        query_body = {
            'query':{
                'range':{
                    'sensitive':{
                        'from':results['sensitive'],
                        'to': 100000
                    }
                }
            }
        }
        influence_rank = es.count(index='sensitive_user_portrait', doc_type='user', body=query_body)
        if influence_rank['_shards']['successful'] != 0:
            return_results['sensitive_rank'] = influence_rank['count']
        else:
            return_results['sensitive_rank'] = 0
    else:
        return_results['sensitive_rank'] = 0
    return_results['sensitive'] = results['sensitive']

    query_body = {
        'query':{
            "match_all":{}
        }
    }
    all_count = es.count(index='sensitive_user_portrait', doc_type='user', body=query_body)
    if all_count['_shards']['successful'] != 0:
        return_results['all_count'] = all_count['count']
    else:
        print 'es_sensitive_user_portrait error'
        return_results['all_count'] = 0

    # link
    link_ratio = results['link']
    return_results['link'] = link_ratio

    weibo_trend = get_user_trend(uid)[0]
    return_results['time_description'] = active_time_description(weibo_trend)
    return_results['time_trend'] = weibo_trend

    # user influence trend
    influence_detail = []
    influence_value = []
    attention_value = []
    ts = time.time()
    ts = datetime2ts('2013-09-08') - 8*24*3600
    for i in range(1,8):
        date = ts2datetime(ts + i*24*3600).replace('-', '')
        detail = [0]*10
        try:
            item = es.get(index=date, doc_type='bci', id=uid)['_source']
            '''
            if return_results['utype']:
                detail[0] = item.get('s_origin_weibo_number', 0)
                detail[1] = item.get('s_retweeted_weibo_number', 0)
                detail[2] = item.get('s_origin_weibo_retweeted_total_number', 0) + item.get('s_retweeted_weibo_retweeted_total_number', 0)
                detail[3] = item.get('s_origin_weibo_comment_total_number', 0) + item.get('s_retweeted_weibo_comment_total_number', 0)
            else:
            '''
            if 1:
                detail[0] = item.get('origin_weibo_number', 0)
                detail[1] = item.get('retweeted_weibo_number', 0)
                detail[2] = item.get('origin_weibo_retweeted_total_number', 0) + item.get('retweeted_weibo_retweeted_total_number', 0)
                detail[3] = item.get('origin_weibo_comment_total_number', 0) + item.get('retweeted_weibo_comment_total_number', 0)
                retweeted_id = item.get('origin_weibo_top_retweeted_id', '0')
                detail[4] = retweeted_id
                if retweeted_id:
                    try:
                        detail[5] = es.get(index='sensitive_user_text', doc_type='user', id=retweeted_id)['_source']['text']
                    except:
                        detail[5] = ''
                else:
                    detail[5] = ''
                detail[6] = item.get('origin_weibo_retweeted_top_number', 0)
                detail[7] = item.get('origin_weibo_top_comment_id', '0')
                if detail[7]:
                    try:
                        detail[8] = es.get(index='sensitive_user_text', doc_type='user', id=detail[7])['_source']['text']
                    except:
                        detail[8] = ''
                else:
                    detail[8] = ''
                detail[9] = item.get('origin_weibo_comment_top_number', 0)
                attention_number = detail[2] + detail[3]
                attention = 2/(1+math.exp(-0.005*attention_number)) - 1
            influence_value.append([date, item['user_index']])
            influence_detail.append([date, detail])
            attention_value.append(attention)
        except:
            influence_value.append([date, 0])
            influence_detail.append([date, detail])
            attention_value.append(0)
    return_results['influence_trend'] = influence_value
    return_results['common_influence_detail'] = influence_detail
    return_results['attention_degree'] = attention_value

    return return_results


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
    utype = user_type(uid)
    if not utype:
        results['utype'] = 0
        return results
    results['utype'] = 1

    # sensitive weibo number statistics
    date = ts2datetime(time.time()-24*3600).replace('-', '')
    date = '20130907' # test
    influence_results = []
    try:
        influence_results = es.get(index=date, doc_type='bci', id=uid)['_source']
        results['sensitive_origin_weibo_number'] = influence_results.get('s_origin_weibo_number', 0)
        results['sensitive_retweeted_weibo_number'] = influence_results.get('s_retweeted_weibo_number', 0)
        results['sensitive_comment_weibo_number'] = influence_results.get('s_comment_weibo_number', 0)
        results['sensitive_retweeted_total_number'] = influence_results.get('s_retweeted_weibo_retweeted_total_number', 0)+influence_results.get('s_origin_weibo_retweeted_total_number', 0)
        results['sensitive_comment_total_number'] = influence_results.get('s_origin_weibo_comment_total_number', 0) + influence_results.get('s_retweeted_weibo_comment_total_number', 0)
    except:
        results['sensitive_origin_weibo_number'] = 0
        results['sensitive_retweeted_weibo_number'] = 0
        results['sensitive_comment_weibo_number'] = 0
        results['sensitive_retweeted_total_number'] = 0
        results['sensitive_comment_total_number'] = 0

    results['sensitive_text'] = sort_sensitive_text(uid)
    results['sensitive_time_trend'] = get_user_trend(uid)[1]

    results['sensitive_geo_distribute'] = []
    results['sensitive_time_distribute'] = get_user_trend(uid)[1]
    results['sensitive_hashtag'] = []
    results['sensitive_words'] = []
    results['sensitive_hashtag_dict'] = []
    results['sensitive_words_dict'] = []
    results['sensitive_hashtag_description'] = ''

    if 1:
        portrait_results = es.get(index="sensitive_user_portrait", doc_type='user', id=uid)['_source']
        temp_hashtag = portrait_results['sensitive_hashtag_dict']
        temp_sensitive_words = portrait_results['sensitive_words_dict']
        temp_sensitive_geo =  portrait_results['sensitive_geo_activity']
        if temp_sensitive_geo:
            sensitive_geo_dict = json.loads(temp_sensitive_geo)
            if len(sensitive_geo_dict) < 7:
                ts = time.time()
                ts = datetime2ts('2013-09-08') - 8*24*3600
                for i in range(7):
                    ts = ts + 24*3600
                    date = ts2datetime(ts).replace('-', '')
                    if sensitive_geo_dict.has_key(date):
                        pass
                    else:
                        sensitive_geo_dict[date] = {}
            sorted_sensitive_geo = sorted(sensitive_geo_dict.items(), key=lambda x:x[0], reverse=False)
            sensitive_geo_list = []
            for k,v in sorted_sensitive_geo:
                temp_list = []
                sorted_geo = sorted(v.items(), key=lambda x:x[1], reverse=True)[0:2]
                # print sorted_geo
                temp_list.extend([k, sorted_geo])
                sensitive_geo_list.append(temp_list)
            results['sensitive_geo_distribute'] = sensitive_geo_list
        if temp_hashtag:
            hashtag_dict = json.loads(portrait_results['sensitive_hashtag_dict'])
            if len(hashtag_dict) < 7:
                ts = time.time()
                ts = datetime2ts('2013-09-08') - 8*24*3600
                for i in range(7):
                    ts = ts + 24*3600
                    date = ts2datetime(ts).replace('-', '')
                    if hashtag_dict.has_key(date):
                        hashtag_dict_detail = hashtag_dict[date]
                        hashtag_dict[date] = sorted(hashtag_dict_detail.items(), key=lambda x:x[1], reverse=True)
                    else:
                        hashtag_dict[date] = {}
            results['sensitive_hashtag_description'] = hashtag_description(hashtag_dict)
        else:
            hashtag_dict = {}
        if temp_sensitive_words:
            sensitive_words_dict = json.loads(temp_sensitive_words)
            if len(sensitive_words_dict) < 7:
                ts = time.time()
                ts = datetime2ts('2013-09-08') - 8*24*3600
                for i in range(7):
                    ts = ts + 24*3600
                    date = ts2datetime(ts).replace('-', '')
                    if sensitive_words_dict.has_key(date):
                        pass
                    else:
                        sensitive_words_dict[date] = {}
        else:
            sensitive_words_dict = {}
        date = ts2datetime(time.time()-24*3600).replace('-', '')
        date = '20130907'
        today_sensitive_words = sensitive_words_dict.get(date,{})
        results['today_sensitive_words'] = json.dumps(today_sensitive_words)
        all_hashtag_dict = {}
        for item in hashtag_dict:
            detail_hashtag_dict = hashtag_dict[item]
            for key in detail_hashtag_dict:
                if all_hashtag_dict.has_key(key[0]):
                    all_hashtag_dict[key[0]] += key[1]
                else:
                    all_hashtag_dict[key[0]] = key[1]

        all_sensitive_words_dict = {}
        for item in sensitive_words_dict:
            detail_words_dict = sensitive_words_dict[item]
            for key in detail_words_dict:
                if all_sensitive_words_dict.has_key(key):
                    all_sensitive_words_dict[key] += detail_words_dict[key]
                else:
                    all_sensitive_words_dict[key] = detail_words_dict[key]

        sorted_hashtag = sorted(all_hashtag_dict.items(), key = lambda x:x[1], reverse=True)
        sorted_words = sorted(all_sensitive_words_dict.items(), key = lambda x:x[1], reverse=True)
        sorted_hashtag_dict = sorted(hashtag_dict.items(), key = lambda x:x[0], reverse=False)
        sorted_words_dict = sorted(sensitive_words_dict.items(), key = lambda x:x[0], reverse=False)
        new_sorted_dict = sort_sensitive_words(sorted_words)
        results['sensitive_hashtag'] = json.dumps(sorted_hashtag)
        results['sensitive_words'] = json.dumps(new_sorted_dict)
        results['sensitive_hashtag_dict'] = json.dumps(sorted_hashtag_dict)
        results['sensitive_words_dict'] = json.dumps(sorted_words_dict)

    results['sensitive_retweet'] = search_retweet(uid, 1)
    results['sensitive_follow'] = search_follower(uid, 1)
    results['sensitive_at'] = search_mention(uid, 1)

    return results
