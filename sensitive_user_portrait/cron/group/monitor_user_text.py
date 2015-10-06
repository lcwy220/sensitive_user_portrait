# -*- coding: UTF-8 -*-
'''
use to compute the mid-result about monitor task
'''
import sys
import time
reload(sys)
sys.path.append('../../')
from global_utils import es_sensitive_user_portrait as es
from global_utils import G_GROUP as r
from global_utils import G_GROUP_TASK as r_task
from time_utils import datetime2ts, ts2datetime

text_index_name = 'monitor_user_text'
text_index_type = 'text'

group_index_name = 'group_result'
group_index_type = 'group'

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
    return task_user

#task_user: one; compute mid result, time_segment is start_ts---start_ts+900
def compute_mid_result_one(task_name, task_user, start_ts):
    result = []
    #step1: count the sensitive or not weibo count
    #step2: count the sensitive or not weibo geo count
    #step3: sensitive words score
    #save mid_result
    status = save_mid_result(task_name, result)
    return status

# save mid-result to es----group_result
def save_mid_result(result):
    status = 0
    return status

# task_user: group; compute mid result, time_segment is start_ts----start_ts+900
def compute_mid_result_group(task_name, task_user, start_ts):
    result = []
    status = save_mid_result(task_name, result)
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
    main()

