# -*- coding:utf-8 -*-

import sys
import time
import redis
from elasticsearch import Elasticsearch
from attribute_from_flow import get_flow_information, temporary_text_update
from user_profile import get_profile_information

reload(sys)
sys.path.append('./../../')
from global_utils import R_RECOMMENTATION as r
from global_utils import es_sensitive_user_portrait as es

def week_update_portrait(user_weibo_dict): # {uid: [weibo_text]}
    uid_list = user_weibo_dict.keys()
    register_result = get_profile_information(uid_list) # 背景信息数据更新
    bulk_action = []
    count = 0
    for user in uid_list:
        result = dict()
        weibo_list = user_weibo_dict[user]
        register_dict = register_result[user]
        result.update(register_dict)
        # results['domain'] = attri_domain(weibo_list)
        result['domain'] = 'test_domain'
        result['domain_string'] = "&".join(result['domain'])
        # psycho_status = attr_psycho_status(user, weibo_list)
        psycho_status = {'positive': 0.5, 'negetive':0.2, 'neutral': 0.3}
        result['psycho_status_string'] = '&'.join(psycho_status.keys())
        result['psycho_status'] = json.dumps(psycho_status)
        # topic = attr_topic(weibo_list)
        topic = {'政治': 0.3, '民生':0.7}
        result['topic'] = json.dumps(topic)
        result['topic_string'] = '&'.join(result['topic'].keys())
        # politics_trend = attri_politics(user, weibo_list)
        politics_trend = 'left'
        result['politics_trend'] = politics_trend
        action = {'update':{'_id': str(user)}}
        results = {'doc':result}
        bulk_action.extend([action, results])
        if count % 1000 == 0:
            es.bulk(bulk_action, index='sensitive_user_portrait', doc_type='user', timeout=60)
            bulk_action = []
            print count
    if bulk_action:
        es.bulk(bulk_action, index='sensitive_user_portrait', doc_type='user', timeout=60)
    return '1'


