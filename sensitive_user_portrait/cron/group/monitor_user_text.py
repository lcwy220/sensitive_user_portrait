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

def get_task_name():
    task_name = ''
    return task_name

def get_task_user(task_name):
    task_user = []
    return task_user

def compute_mid_result(task_name, task_user):
    result = []
    status = save_mid_result(result)
    return status

def save_mid_result(result):
    status = 0
    return status


def main():
    #step1: get task from redis queue (rpop and lpush---keep the task is in the queue)
    #setp2: get task user from es---group_result
    #step3: compute task mid-result
    #step4: save the mid-result in mid-result es----timestamp as field
    while True:
        task_name = get_task_name()
        task_user = get_task_user(task_name)
        status = compute_mid_result(task_name, task_user)
        if status == 0:
            print 'there is a bug about %s task' % task_name

if __name__=='__main__':
    main()

