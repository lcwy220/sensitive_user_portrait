#-*- coding:utf-8 -*-
from time_utils import datetime2ts
from global_utils import es_user_portrait as es_weibo_portrait
from Offline_task import add_task

WEIBO_RANK_KEYWORD_TASK_INDEX = 'weibo_rank_keyword_task'
WEIBO_RANK_KEYWORD_TASK_TYPE = 'weibo_rank_task'

def weibo_sort_interface(username , time, sort_scope, sort_norm, arg, st, et, task_number, number):
    task_number = int(task_number)
    print "user_interface:", number

    weibo_list = []
    during = (datetime2ts(et) - datetime2ts(st)) / DAY + 1
    time = 1
    if during > 3:
        time = 7
    elif during > 16:
        time = 30

    query_body = {
        "query":{
            "terms":{
                "status": [0, -1]
            }
        }
    }

    if sort_scope == 'all_limit_keyword':
        running_number = es_weibo_portrait.count(index=WEIBO_RANK_KEYWORD_TASK_INDEX, doc_type=WEIBO_RANK_KEYWORD_TASK_TYPE, body=query_body)['count']
        if running_number > task_number - 1:
            return "more than limit"
        search_id = add_task(username, type="keyword", during=during, st=st, et=et, arg=arg, sort_norm=sort_norm, sort_scope=sort_scope, time=time, number=number)
        #deal with the offline task   
        return {"flag": True , "search_id": search_id}

    elif sort_scope == 'all_nolimit':
        pass

    return weibo_list
