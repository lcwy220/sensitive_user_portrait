# -*- coding: UTF-8 -*-
'''
the functions about the track task
'''
import sys
import time
import json
'''
reload(sys)
sys.path.append('../')
from global_utils import G_GROUP as r
from global_utils import G_GROUP_TASK as r_task
from global_utils import es_user_portrait as es
'''
from sensitive_user_portrait.global_utils import R_GROUP as r
from sensitive_user_portrait.global_utils import R_GROUP_TASK as r_task
from sensitive_user_portrait.global_utils import es_sensitive_user_portrait as es

index_name = 'group_result'
index_type = 'group'

# submit track task to es
def submit_track_task(input_data):
    '''
    step1: identify the task_name is not exist
    step2: index new task_name
    step3: add user list to redis???---should identify
    step4: add task to redis queue
    '''
    status = 0
    task_name = input_data['task_name']
    try:
        result = es.get(index=index_name, doc_type=index_type, id=task_name)['_source']
        return 'task_name exist'
    except:
        es.index(index=index_name, doc_type=index_type, id=task_name, body=input_data)
        task_user = input_data['uid_list']
        status = add_user_set(task_user)
        if status == 0:
            return 'add user to redis set fail'
        else:
            status = add_task_redis(task_name)
            if status == 0:
                return 'add task to redis fail'
            else:
                return 'success submit'

# add track task to reis
def add_task_redis(task_name):
    status = 0
    result = r_task.lpush('monitor_task', task_name)
    if result != 0:
        status = 1
    return status

# delete track task from redis when the task is end or delete
def delete_task_redis(task_name):
    status = 0
    result = r_task.lrem('monitor_task', 0, task_name)
    if result != 0:
        status = 1
    return status

# add user to redis set where keep user to track
'''
step1: identify the user is or not in track user set
step2: add user task count
data: {'track_task_user': {uid: task_count}}
'''
def add_user_set(user_list):
    status = 0
    for uid in user_list:
        r.hincrby('track_task_user', str(uid))
    status = 1
    return status

def search_track_task(task_name, submit_date, state, status):
    result = []
    query = []
    condition_num = 0
    if task_name:
        task_name_list = task_name.split(' ')
        for item in task_name_list:
            query.append({'wildcard': {'task_name': '*' + item + '*'}})
            condition_num += 1
    if submit_date:
        query.append({'match': {'submit_date': submit_date}})
        condition_num += 1
    if state:
        state_list = state.split(' ')
        for item in state_list:
            query.append({'wildcard': {'state': '*' + item + '*'}})
            condition_num += 1
    if status:
        query.append({'match': {'status': status}})
        condition_num += 1
    if condition_num > 0:
        try:
            source = es.search(
                    index = 'group_result',
                    doc_type = 'group',
                    body = {
                        'query':{
                            'bool':{
                                'must':query
                                }
                            },
                        'size': 100000
                        }
                    )
        except Exception as e:
            raise e
    else:
        source = es.search(
                index = 'group_result',
                doc_type = 'group',
                body = {
                    'query':{'match_all':{}
                        },
                    'size': 100000
                    }
                )
    try:
        task_dict_list = source['hits']['hits']
    except:
        return None
    #print 'task_dict_list:', task_dict_list
    for task_dict in task_dict_list:
        #print 'task_dict:', task_dict['_source'], type(task_dict)
        result.append([task_dict['_source']['task_name'], task_dict['_source']['submit_date'], task_dict['_source']['count'], task_dict['_source']['state'],task_dict['_source']['status']])
    #print 'result:', result
    return result

# get track task result
'''
step1: get task from es and get uid list
step2: from mid-result to get finally result----should identify
'''
def get_track_result(task_name, module):
    result = {}
    return result

# end track task result
'''
step1: identify the task exist and status is 1
step2: change the task status from 1 to 0
step3: delete the task from redis queue
'''
def end_track_task(task_name):
    status = 0
    try:
        task_exist = es.get(index=index_name, doc_type=index_type, id=task_name)['_source']
    except:
        return 'task name not exist'
    task_status = task_exist['status']
    if status == '0':
        return 'task have end'
    else:
        task_exist['status'] = 0
        task_user = task_exist['uid_list']
        status = change_user_count(task_user)
        if status == 0:
            return 'change user task count fail'
        else:
            es.index(index=index_name, doc_type=index_type, id=task_name, body=task_exist)
            status = delete_task_redis(task_name)
            if status == 0:
                return 'delete task from redis fail'
            else:
                return 'success change status to end'


# track task user in redis set
# data: {uid: task_count}
def change_user_count(task_user):
    status = 0
    for uid in task_user:
        uid_task_count = r.hget('track_task_user', str(uid))
        if int(uid_task_count) >1:
            r.hincrby('track_task_user', str(uid), -1)
        else:
            r.hdel('track_task_user', str(uid))
    status = 1
    return status


'''
step1: identify the task exist
step2: delete the task user from redis
step3: delete the task from es
'''
def delete_track_task(task_name):
    status = 0
    try:
        task_exist = es.get(index=index_name, doc_type=index_type, id=task_name)['_source']
    except:
        return 'task not exist'
    task_user = task_exist['uid_list']
    #change the user task_count in redis set
    #status = change_user_count(task_user)
    status = 1
    if status==0:
        return 'change user count fail'
    else:
        #delete task from es
        result = es.delete(index=index_name, doc_type=index_type, id=task_name)
        status = delete_task_redis(task_name)
        if status == 0:
            return 'delete task from redis fail'
        else:
            return 'success delete task'

