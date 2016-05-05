# -*- coding:utf-8 -*-

import sys
import time
import redis
from elasticsearch import Elasticsearch
from attribute_from_flow import get_flow_information, temporary_text_update
from evaluate_index import get_evaluate_index

reload(sys)
sys.path.append('./../../')
from global_utils import R_RECOMMENTATION as r
from global_utils import es_sensitive_user_portrait as es

def daily_update_portrait(user_weibo_dict): # {uid: [weibo_text]}
    uid_list = user_weibo_dict.keys()
    bulk_action = []
    count = 0
    for user in uid_list:
        results = dict()
        weibo_list = user_weibo_dict[user]
        flow_result = get_flow_information(user)
        text_result = temporary_text_update(user, weibo_list)
        evaluate_result = evaluate_index(user, status='update')
        results.update(flow_result)
        results.update(text_result)
        results.update(evaluate_result)
        action = {'update':{'_id': str(user)}}
        result = {'doc':results}
        bulk_action.extend([action, result])
        if count % 1000 == 0:
            es.bulk(bulk_action, index='sensitive_user_portrait', doc_type='user', timeout=60)
            bulk_action = []
            print count
    if bulk_action:
        es.bulk(bulk_action, index='sensitive_user_portrait', doc_type='user', timeout=60)
    return '1'


