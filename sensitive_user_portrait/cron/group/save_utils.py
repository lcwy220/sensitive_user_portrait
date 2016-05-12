# -*- coding: UTF-8 -*-
import sys
import time
import json
reload(sys)
sys.path.append('../../')
from global_utils import es_group_result as es
from global_utils import group_index_name as index_name
from global_utils import group_index_type as index_type


def save_group_results(results):
    status = False
    submit_user = results['submit_user']
    task_name = results['task_name']
    task_id = submit_user + '-' + task_name
    #step1: identify the task is exist
    try:
        task_exist_result = es.get(index=index_name, doc_type=index_type, id=task_id)['_source']
    except:
        task_exist_result = {}

    #step2: save result
    if task_exist_result != {}:
        es.index(index=index_name, doc_type=index_type, body=results, id=task_id)
        status = True

    return status


