# -*- coding: UTF-8 -*-
'''
use to compute the mid-result about monitor task
'''
import sys
import time
import json
reload(sys)
sys.path.append('../../')
from global_utils import es_sensitive_user_portrait as es
from global_utils import R_GROUP as r
from global_utils import R_GROUP_TASK as r_task
from global_utils import MONITOR_INNER_REDIS as monitor_inner_r
from time_utils import datetime2ts, ts2datetime, ts2date

text_index_name = 'monitor_user_text'
text_index_type = 'text'

group_index_name = 'group_result'
group_index_type = 'group'

monitor_index_name = 'monitor_result'
#monitor_index_type:  task_name

# keep task queue in redis
def get_task_name():
    task_name = ''
    task_name = r_task.rpop('monitor_task')
    return task_name

# keep task queue in redis
def add_task_name(task_name):
    status = r_task.lpush('monitor_task', task_name)
    return status

# get task user from group_result es
def get_task_user(task_name):
    print 'get_task_user'
    task_user = []
    try:
        task_dict = es.get(index=group_index_name, doc_type=group_index_type, id=task_name)['_source']
    except:
        return None
    task_user = task_dict['uid_list']
    if isinstance(task_user, list)==False:
        task_user = [task_user]
    print 'task_user:', task_user
    return task_user

#task_user: one; compute mid result, time_segment is start_ts---start_ts+900
def compute_mid_result_one(task_name, task_user, start_ts):
    result = []
    #step1: count the sensitive or not weibo count
    #step2: count the sensitive or not weibo geo count
    #step3: sentiment in sensitive / unsensitive
    #step4: compute hashtag
    #step5: compute sensitive_word
    #save mid_result
    query_body = []
    #query user
    query_body.append({'term':{'uid': task_user[0]}})
    #query time_segment
    query_body.append({'range':{'timestamp':{'from':start_ts, 'to':start_ts+900}}})
    try:
        task_user_weibo = es.search(index=text_index_name, doc_type=text_index_type,\
            body={'query':{'bool':{'must': query_body}}, 'size':100000})['hits']['hits']
    except Exception,e:
        raise e
    
    sensitive_weibo_dict = {}
    #sentiment_weibo_dict = {'0':{}, '1':{}}
    #geo_weibo_dict = {'0':{}, '1':{}}
    #hashtag_weibo_dict = {'0':{}, '1':{}}
    sentiment_weibo_dict = {}
    geo_weibo_dict = {}
    hashtag_weibo_dict = {}
    sensitive_word_dict = {}
    search_count = len(task_user_weibo)
    if task_user_weibo:
        for weibo_item in task_user_weibo:
            weibo_dict = weibo_item['_source']
            #compute sensitive_weibo_count and unsensitive_weibo_count in time-segment 
            sensitive = weibo_dict['count']
            try:
                sensitive_weibo_dict[str(sensitive)] += 1
            except:
                sensitive_weibo_dict[str(sensitive)] = 1
            #compute geo_weibo_count
            geo = weibo_dict['geo']
            if str(sensitive) in geo_weibo_dict:
                try:
                    geo_weibo_dict[str(sensitive)][geo] += 1
                except:
                    geo_weibo_dict[str(sensitiive)][geo] = 1
            else:
                geo_weibo_dict[str(sensitive)] = {geo: 1}
            #compute sentiment_weibo_count
            sentiment = weibo_dict['sentiment']
            if str(sensitive) in sentiment_weibo_dict:
                try:
                    sentiment_weibo_dict[str(sensitive)][sentiment] += 1
                except:
                    sentiment_weibo_dict[str(sensitive)][sentiment] = 1
            else:
                sentiment_weibo_dict[str(sensitive)] = {sentiment: 1}
            #compute hashtag
            try:
                hashtag_list = weibo_dict['hashtag'].split('&')
            except:
                hashtag_list = None
            if hastag_list:
                for hashtag in hashtag_list:
                    if str(sensitive) in hashtag_weibo_dict:
                        try:
                            hashtag_weibo_dict[str(sensitive)][hashtag] += 1
                        except:
                            hashtag_weibo_dict[str(sensitive)][hashtag] = 1
                    else:
                        hashtag_weibo_dict[str(sensitive)] = {hashtag: 1}
            
            #compute sensitive_word
            try:
                sensitive_word_list = weibo_dict['sensitive_word'].split('&')
            except:
                sensitive_word_list = None
            if sensitive_word_list:
                for word in senstive_word_list:
                    try:
                        sensitive_word_dict[word] += 1
                    except:
                        sensitive_word_dict[word] = 1

    if search_count != 0:
        status = save_mid_result_one(task_name, sensitive_weibo_dict, geo_weibo_dict, sentiment_weibo_dict, hashtag_weibo_dict, sensitive_word_dict, start_ts)
    else:
        status = 1
    return status

# save task: one  mid-result to es----group_result
def save_mid_result_one(task_name, sensitive_weibo_dict, geo_weibo_dict, sentiment_weibo_dict, hashtag_weibo_dict, sensitive_word_dict, start_ts):
    status = 0
    insert_body = {}
    insert_body['count'] = json.dumps(sensitive_weibo_dict)
    insert_body['geo'] = json.dumps(geo_weibo_dict)
    insert_body['sentiment'] = json.dumps(sentiment_weibo_dict)
    if hashtag_weibo_dict != {}:
        insert_body['hashtag'] = json.dumps(hashtag_weibo_dict)
    if sensitive_word_dict != {}:
        insert_body['sensitive_word'] = json.dumps(sensitive_word_dict)
    insert_body['timestamp'] = start_ts # mark the ts
    
    es.index(index=monitor_index_name, doc_type=task_name, id=start_ts, body=insert_body)
    status = 1
    return status

# task_user: group; compute mid result, time_segment is start_ts----start_ts+900
def compute_mid_result_group(task_name, task_user, start_ts):
    result = []
    #step1: count the sensitive or not weibo count
    #step2: count the geo weibo count
    #step3: count the sentiment weibo count
    #step4: compute hashtag
    #step5: compute sensitive
    #step: compute the social
    #save mid result
    sensitive_weibo_dict = {}
    #sentiment_weibo_dict = {'0':{}, '1':{}}
    #geo_weibo_dict = {'0':{}, '1':{}}
    #hashtag_weibo_dict = {'0':{}, '1':{}}
    sentiment_weibo_dict = {}
    geo_weibo_dict = {}
    hashtag_weibo_dict = {}
    sensitive_word_dict = {}
    search_count = 0
    for uid in task_user:
        query_body = []
        query_body.append({'term':{'uid':str(uid)}})
        query_body.append({'range':{'timestamp':{'from': start_ts, 'to':start_ts+900}}})
        try:
            user_weibo = es.search(index=text_index_name, doc_type=text_index_type, \
                    body={'query':{'bool':{'must':query_body}}, 'size':100000})['hits']['hits']
        except Exception, e:
            raise e
        print 'user_weibo:', len(user_weibo)
        search_count += len(user_weibo)
        if user_weibo:
            for weibo_item in user_weibo:
                weibo_dict = weibo_item['_source']
                #compute sensitive_weibo_count and unsensitive_weibo_count in time-segment
                sensitive = weibo_dict['sensitive']
                try:
                    sensitive_weibo_dict[str(sensitive)] += 1
                except:
                    sensitive_weibo_dict[str(sensitive)] = 1
                #compute geo_weibo_count
                geo = weibo_dict['geo']
                if str(sensitive) in geo_weibo_dict:
                    try:
                        geo_weibo_dict[str(sensitive)][geo] += 1
                    except:
                        geo_weibo_dict[str(sensitive)][geo] = 1
                else:
                    geo_weibo_dict[str(sensitive)] = {geo: 1}
                #compute sentiment_weibo_count
                sentiment = weibo_dict['sentiment']

                if str(sensitive) in sentiment_weibo_dict:
                    try:
                        sentiment_weibo_dict[str(sensitive)][sentiment] += 1
                    except:
                        sentiment_weibo_dict[str(sensitive)][sentiment] = 1
                else:
                    sentiment_weibo_dict[str(sensitive)] = {sentiment: 1}
                #compute hashtag_weibo_dict
                try:
                    hashtag_list = weibo_dict['hashtag'].split('&')
                except:
                    hashtag_list = None
                if hashtag_list:
                    for hashtag in hashtag_list:
                        if str(sensitive) in hashtag_weibo_dict:
                            try:
                                hashtag_weibo_dict[str(sensitive)][hashtag] += 1
                            except:
                                hashtag_weibo_dict[str(sensitive)][hashtag] = 1
                        else:
                            hashtag_weibo_dict[str(sensitive)] = {hashtag: 1}
                #compute sensitive_word_dict
                try:
                    sensitive_word_list = weibo_dict['sensitive_word'].split('&')
                except:
                    sensitive_word_list = None
                if sensitive_word_list:
                    for sensitive_word in sensitive_word_list:
                        try:
                            sensitive_word_dict[sensitive_word] += 1
                        except:
                            sensitive_word_dict[sensitive_word] = 1
    print 'end compute'
    if search_count != 0:
        status = save_mid_result_group(task_name, sensitive_weibo_dict, geo_weibo_dict, \
                sentiment_weibo_dict, hashtag_weibo_dict, sensitive_word_dict, start_ts)
    else:
        status = 1

    return status

# save task: group mid-result to es----group_result
def save_mid_result_group(task_name, sensitive_weibo_dict, geo_weibo_dict, sentiment_weibo_dict, hashtag_weibo_dict, sensitive_word_dict, start_ts):
    status = 0
    print 'start save result to es'
    insert_body = {}
    insert_body['count'] = json.dumps(sensitive_weibo_dict)
    insert_body['geo'] = json.dumps(geo_weibo_dict)
    insert_body['sentiment'] = json.dumps(sentiment_weibo_dict)
    if hashtag_weibo_dict != {}:
        insert_body['hashtag'] = json.dumps(hashtag_weibo_dict)
    if sensitive_word_dict != {}:
        insert_body['sensitive_word'] = json.dumps(sensitive_word_dict)
    insert_body['timestamp'] = start_ts
    # other attribute about monitor group should be add
    es.index(index=monitor_index_name, doc_type=task_name, id=start_ts, body=insert_body)
    status = 1
    print 'end save result'
    return status

#identify task is doing in ES(group_result)
def identify_task_doing(task_name):
    task_doing_status = True
    try:
        task_dict = es.get(index=group_index_name, doc_type=group_index_type, id=task_name)['_source']
    except:
        task_doing_status = False
        return task_doing_status
    status = task_dict['status']
    if status != 1:
        task_doing_status = False

    return task_doing_status


# use to merge to dict
def merge_dict(*objs):
    _keys = set(sum([obj.keys() for obj in objs], []))
    _total = {}
    for _key in _keys:
        _total[_key] = sum([obj.get(_key, 0) for obj in objs])
    return _total


# use to compute inner group polarization
def compute_group_inner(task_name, task_user, start_ts):
    #step1: get task_user in-monitor task user retweet relation from monitor_inner_r
    #step2: get task_user in-task user retweet relation
    #step3: compute every inner user be-retweet ratio in task
    #step4: save top5 to es--monitor_result, doc_type=task_name, _id='inner_'+date  e:'inner_2013-09-01'
    group_status = 0
    time_segment = 3600*24
    iter_ts = start_ts - time_segment
    inner_group_dict = {}
    user_count_dict = {}
    for root_uid in task_user:
        inner_group_dict[root_uid] = {}
        while True:
            if iter_ts >= start_ts:
                break
            key = 'inner_' + str(iter_ts) 
            try:
                inner_retweet_dict = json.loads(monitor_inner_r.hget(root_uid, key))
            except:
                inner_retweet_dict = None
            if inner_retweet_dict:
                inner_group_dict[root_uid] = merge_dict(inner_group_dict[root_uid], inner_retweet_dict)
            iter_ts += time_segment
        user_inner_retweet_count = sum(inner_group_dict[root_uid].values())
        user_count_dict[root_uid] = user_inner_retweet_count
    all_be_retweet_count = sum(user_count_dict.values())
    if all_be_retweet_count==0:
        group_status = 1
        return group_status
    sort_user_inner_retweet_count = sorted(user_count_dict.items(), key=lambda x:x[1], reverse=True)
    top5_user = sort_user_inner_retweet_count[:5]

    # timestamp: '2013-09-01'
    date = ts2datetime(start_ts)
    index_body = {'date': date}
    for rank in range(1,6):
        key = 'top' + str(rank)
        index_body[key] = json.dumps(top5_user[rank-1])
    key = 'inner_' + date
    # save inner-retweet graph by dict {root_uid1:{uid1:count1, uid2:count2}, ...}
    index_body['inner_graph'] = json.dumps(inner_group_dict)
    
    es.index(index=monitor_index_name, doc_type=task_name, id=key, body=index_body)
    group_status = 1
    return group_status

def main():
    #step1: get task from redis queue (rpop)
    #step2: get monitor task time record from redis----data: {'monitor_task_time_record':{task_name, compute_start_ts}}
    #step3: identify the compute_start_ts can be compute
    #setp4: get task user from es---group_result
    #step5: according task user count do differently computing
    #step6: compute task mid-result
    #step7: save the mid-result in mid-result es----timestamp as field
    #step8: identify the track task is doing ,not end/delete  from group_result es status==1 not 0
    #step8: if track_task is doing: update the compute_start_ts
    #step9: if track_task is doing: lpush task name to redis queue (keep the task in queue)
    #step10: if track_task is not doing: delete the compute_start_ts from redis
    while True:
        task_name = get_task_name()
        if task_name:
            start_ts = r_task.hget('monitor_task_time_record', task_name)
            start_ts = int(start_ts)
            #now_ts = time.time()
            #test
            now_ts = datetime2ts('2013-09-08')
            if start_ts == now_ts:
                status = add_task_name(task_name)
                if status == 0:
                    print 'add task to redis fail'
                    break

            if start_ts + 900 <= now_ts:
                task_user  = get_task_user(task_name)
                
                if len(task_user)==1:
                    print 'compute %s start_ts %s' % (task_name, ts2date(start_ts))
                    status = compute_mid_result_one(task_name, task_user, start_ts)
                else:
                    print 'compute %s start_ts %s' % (task_name, ts2date(start_ts))
                    status = compute_mid_result_group(task_name, task_user, start_ts)
                    #compute group polarization----compute once a day
                    if datetime2ts(ts2datetime(start_ts)) == start_ts:
                        print 'start commpute group inner %s' % ts2date(start_ts)
                        group_status = compute_group_inner(task_name, task_user, start_ts)
                        status += group_status

                if status == 0:
                    print 'there is a bug about %s task' % task_name
                else:
                    #update the record time
                    start_ts += 900
                    task_doing_status = identify_task_doing(task_name)
                    print 'task_doing_status:', task_doing_status
                    if task_doing_status == True:
                        r_task.hset('monitor_task_time_record', task_name, start_ts)
                        status = add_task_name(task_name)
                        if status==0:
                            print 'add task name to redis fail'
                    else:
                        r_task.hdel('monitor_task_time_record', task_name)

if __name__=='__main__':
    main()
    '''
    task_name = 'test2'
    sensitive_weibo_dict = {'0':1, '1':2}
    geo_weibo_dict = {'city1':1, 'city2':2}
    sentiment_weibo_dict = {'126':1, '130':2}
    start_ts = 1429215300
    hashtag_weibo_dict = {'hashtag1':1}
    sensitive_word_dict = {'word1':1, 'word2':2}

    save_mid_result_one(task_name, sensitive_weibo_dict, geo_weibo_dict, sentiment_weibo_dict, hashtag_weibo_dict, sensitive_word_dict, start_ts)
    '''
    task_name = 'testtask'
    #add_task_name(task_name)
    #test
    #es.delete(index=monitor_index_name, doc_type='testtask2', id='inner_2013-09-01')
