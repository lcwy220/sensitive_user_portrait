# -*- coding: UTF-8 -*-
'''
use to get track result by module
'''
import sys
import time
import json
from sensitive_user_portrait.global_utils import es_sensitive_user_portrait as es
from sensitive_user_portrait.global_utils import MONITOR_REDIS


# identify the task_name exist
def identify_task(task_name):
    task_status = False
    task_user = []
    return task_status, task_user

# show basic information
def get_basic_result(task_name):
    result = []
    return result

# show time information---sensitive weibo count and unsensitive weibo count
def get_time_result(task_name):
    result = []
    return result

# show sentiment information----sensitive weibo or unsensitive
def get_sentiment_result(task_name):
    result = []
    return result

# show sensitive information
def get_setiment_result(task_name):
    result = []
    return result

# show sensitive score trend
def get_sensitive_result(task_name):
    result = []
    return result

# show geo result
def get_geo_result(task_name):
    result = []
    return result

# show hashtag result
def get_hashtag_result(task_name):
    result = []
    return result

# show network result
def get_network_result(task_name):
    result = []
    return result

def get_track_result(task_name, module):
    #step1: identify the task_name is in ES(group_result)
    #step2: based on the module to get result

    task_status, task_user = identify_task(task_name)
    if task_status == False:
        return 'the task is not exist'
    if module == 'basic':
        result = get_basic_result(task_name)
    elif module == 'time':
        result = get_time_result(task_name)
    elif module == 'sentiment':
        result = get_sentiment_result(task_name)
    elif module == 'sensitive':
        result = get_sensitive_result(task_name)
    elif module == 'geo':
        result = get_geo_result(task_name)
    elif module == 'hashtag':
        result = get_hashtag_result(task_name)
    elif module == 'network':
        result = get_network_result(task_name)
    else:
        return 'no this module'
    return result


