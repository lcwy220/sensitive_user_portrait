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
from time_utils import datetime2ts, ts2datetime

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
    task_user = []
    try:
        task_dict = es.get(index=group_index_name, doc_type=group_index_type, id=task_name)['_source']
    except:
        return None
    task_user = task_dict['uid_list']
    if isinstance(task_user, list)==False:
        task_user = [task_user]
    return task_user

#task_user: one; compute mid result, time_segment is start_ts---start_ts+900
def compute_mid_result_one(task_name, task_user, start_ts):
    result = []
    #step1: count the sensitive or not weibo count
    #step2: count the sensitive or not weibo geo count
    #step3: sensitive words score
    #step4: compute hashtag
    #step5: compute sensitive_word
    #save mid_result
    query_body = []
    #query user
    query_body.append({'term':{'uid': int(task_user[0])}})
    #query time_segment
    query_body.append({'range':{'timestamp':{'from':start_ts, 'to':start_ts+900}}})
    try:
        task_user_weibo = es.search(index=text_index_name, doc_type=text_index_type,\
            body={'query':{'bool':{'must': query_body}}, 'size':100000})['hits']['hits']
    except Exception,e:
        raise e
    
    sensitive_weibo_dict = {}
    sentiment_weibo_dict = {'0':{}, '1':{}}
    geo_weibo_dict = {'0':{}, '1':{}}
    hashtag_weibo_dict = {'0':{}, '1':{}}
    sensitive_word_dict = {}
    if task_user_weibo:
        for weibo_item in task_user_weibo:
            weibo_dict = weibo_item['_source']
            #compute sensitive_weibo_count and unsensitive_weibo_count in time-segment 
            sensitive = weibo_dict['sensitive']
            try:
                sensitive_weibo_dict[str(sensitive)] += 1
            except:
                sensitive_weibo_dict[str(sensitive)] = 1
            #compute geo_weibo_count
            geo = weibo_dict['geo']
            try:
                geo_weibo_dict[str(sensitive)][geo] += 1
            except:
                geo_weibo_dict[str(sensitiive)][geo] = 1
            #compute sentiment_weibo_count
            sentiment = weibo_dict['sentiment']
            try:
                sentiment_weibo_dict[str(sensitive)][sentiment] += 1
            except:
                sentiment_weibo_dict[str(sensitive)][sentiment] = 1
            #compute hashtag
            try:
                hashtag_list = weibo_dict['hashtag'].split('&')
            except:
                hashtag_list = None
            if hastag_list:
                for hashtag in hashtag_list:
                    try:
                        hashtag_weibo_dict[str(sensitive)][hashtag] += 1
                    except:
                        hashtag_weibo_dict[str(sensitive)][hashtag] = 1
            
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


    status = save_mid_result_one(task_name, sensitive_weibo_dict, geo_weibo_dict, sentiment_weibo_dict, hashtag_weibo_dict, sensitive_word_dict, start_ts)
    return status

# save task: one  mid-result to es----group_result
def save_mid_result_one(task_name, sensitive_weibo_dict, geo_weibo_dict, sentiment_weibo_dict, hashtag_weibo_dict, sensitive_word_dict, start_ts):
    status = 0
    insert_body = {}
    insert_body['count'] = json.dumps(sensitive_weibo_dict)
    insert_body['geo'] = json.dumps(geo_weibo_dict)
    insert_body['sentiment'] = json.dumps(sentiment_weibo_dict)
    if hashtag_weibo_dict != {'0':{}, '1':{}}:
        insert_body['hashtag'] = json.dumps(hashtag_weibo_dict)
    if sensitive_word_dict :
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
    sentiment_weibo_dict = {'0':{}, '1':{}}
    geo_weibo_dict = {'0':{}, '1':{}}
    hashtag_weibo_dict = {'0':{}, '1':{}}
    sensitive_word_dict = {}
    for uid in task_user:
        query_body = []
        query_body.append({'term':{'uid':uid}})
        query_body.append({'range':{'timestamp':{'from': start_ts, 'to':start_ts+900}}})
        try:
            user_weibo = es.search(index=text_index_name, doc_type=text_index_type, \
                    body={'query':{'bool':{'must':query_body}}, 'size':100000})['hits']['hits']
        except Exception, e:
            raise e

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
                try:
                    geo_weibo_dict[str(sensitive)][geo] += 1
                except:
                    geo_weibo_dict[str(sensitive)][geo] = 1
                #compute sentiment_weibo_count
                sentiment = weibo_dict['sentiment']
                try:
                    sentiment_weibo_dict[str(sensitive)][sentiment] += 1
                except:
                    sentiment_weibo_dict[str(sensitive)][sentiment] = 1
                #compute hashtag_weibo_dict
                try:
                    hashtag_list = weibo_dict['hashtag'].split('&')
                except:
                    hashtag_list = None
                if hashtag_list:
                    for hashtag in hashtag_list:
                        try:
                            hashtag_weibo_dict[str(sensitive)][hashtag] += 1
                        except:
                            hashtag_weibo_dict[str(sensitive)][hashtag] = 1
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
    
    status = save_mid_result_group(task_name, sensitive_weibo_dict, geo_weibo_dict, \
            sentiment_weibo_dict, hashtag_weibo_dict, sensitive_weibo_dict, start_ts)

    return status

# save task: group mid-result to es----group_result
def save_mid_result_group(task_name, sensitive_weibo_dict, geo_weibo_dict, sentiment_weibo_dict, hashtag_weibo_dict, sensitive_weibo_dict, start_ts):
    status = 0
    insert_body = {}
    insert_body['sensitive'] = json.dumps(sensitive_weibo_dict)
    insert_body['geo'] = json.dumps(geo_weibo_dict)
    insert_body['sentiment'] = json.dumps(sentiment_weibo_dict)
    if hashtag_weibo_dict != {'0':{}, '1':{}}:
        insert_body['hashtag'] = json.dumps(hashtag_weibo_dict)
    if sensitive_weibo_dict:
        insert_body['sentiment_word'] = json.dumps(sentiment_weibo_dict)
    insert_body['timestamp'] = start_ts
    # other attribute about monitor group should be add
    es.index(index=monitor_index_name, doc_type=task_name, id=start_ts, body=insert_body)
    status = 1
    return status

#identify task is doing in ES(group_result)
def identify_task_doing(task_name):
    task_doing_status = True
    try:
        task_dict = es.get(index=group_index_name, doc_type=group_index_type, id=task_name)['source']
    except:
        task_doing_status = False
        return task_doing_status
    status = task_dict['status']
    if status != 1:
        task_doing_status = False

    return task_doing_status


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
            now_ts = time.time()
            if start_ts + 900 < now_ts:
                task_user  = get_task_user(task_name)
                if len(task_user)==1:
                    status = compute_mid_result_one(task_name, task_user, start_ts)
                else:
                    status = compute_mid_result_group(task_name, task_user, start_ts)
                if status == 0:
                    print 'there is a bug about %s task' % task_name
                else:
                    #update the record time
                    start_ts += 900
                    task_doing_status = identify_task_doing(task_name)
                    if task_doing_status == True:
                        r_task.hset('monitor_task_time_record', task_name, start_ts)
                        status = add_task_name(task_name)
                        if status==0:
                            print 'add task name to redis fail'
                    else:
                        r_task.hdel('monitor_task_time_record', task_name)

if __name__=='__main__':
    #main()
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
    
