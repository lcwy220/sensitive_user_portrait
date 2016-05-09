# -*- coding:utf-8 -*-

# 本程序定时启动，是监控任务的入口，从manag es中读取尚未完成的任务，送入redis的任务队列中，
# 由子程序从队列中pop出任务信息进行监控计算

import sys
import time
import json
import copy
import os
from social_sensing import social_sensing_task 
reload(sys)
sys.path.append("../../")
from global_utils import es_user_profile as es_profile
from global_utils import R_SOCIAL_SENSING as r
from global_utils import es_user_portrait as es
from time_utils import ts2datetime, datetime2ts, ts2date, ts2date_hour, date_hour2ts
from parameter import DOC_TYPE_MANAGE_SOCIAL_SENSING as task_doc_type
from parameter import INDEX_MANAGE_SOCIAL_SENSING as index_name

def create_task_list():
    # 1. search from manage_sensing_task
    # 2. push to redis list-----task_work

    # print start info
    current_path = os.getcwd()
    file_path = os.path.join(current_path, 'task_list.py')
    #now_ts = date_hour2ts(ts2date_hour(time.time()))
    now_ts = 1378011600 # 1378008000
    print_log = "&".join([file_path, "start", ts2date(now_ts)])
    print print_log
    #ts = ts - 3600

    query_body = {
        "query":{
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"term":{"finish": "0"}},
                            {"term":{"processing_status": "1"}}
                        ]
                    }
                }
            }
        }
    }

    search_results = es.search(index=index_name, doc_type=task_doc_type, body=query_body)['hits']['hits']

    count = 0
    if search_results:
        for iter_item in search_results:
            _id = iter_item['_id']
            item = iter_item['_source']
            task = []
            task.append(item['task_name']) # task_name
            task.append(item['keywords']) # keywords
            task.append(item['stop_time']) # stop time
            task.append(item['create_by'])
            task.append(now_ts)
            r.lpush('task_name', json.dumps(task))
            count += 1

    print count
    print_log = "&".join([file_path, "end", ts2date(time.time())])
    print print_log


if __name__ == "__main__":
    create_task_list()
    social_sensing_task()

