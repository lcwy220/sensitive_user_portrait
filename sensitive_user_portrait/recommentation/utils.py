# -*- coding:utf-8 -*-

import redis
import sys
import time
import datetime
import json
import IP
from elasticsearch import Elasticsearch
from sensitive_user_portrait.global_utils import R_RECOMMENTATION as r
from sensitive_user_portrait.global_utils import R_CLUSTER_FLOW2 as r_cluster
from sensitive_user_portrait.global_utils import ES_CLUSTER_FLOW1 as es_cluster
from sensitive_user_portrait.global_utils import es_user_profile
from sensitive_user_portrait.global_utils import es_sensitive_user_portrait
from sensitive_user_portrait.time_utils import ts2datetime, datetime2ts

# obtain user detail information, such as uid,nickname,location,fansnum,statusnum,influence,weibo_mid
def get_sensitive_user_detail(uid_list, date, sensitive):
    results = []
    index_name = str(date).replace('-','') # index_name:20130901
    user_bci_results = es_cluster.mget(index=index_name, doc_type='bci', body={'ids':uid_list}, _source=True)['docs']
    user_profile_results = es_user_profile.mget(index="weibo_user", doc_type="user", body={"ids":uid_list}, _source=True)['docs']
    for i in range(0, len(uid_list)):
        personal_info = ['']*5
        uid = uid_list[i]
        personal_info[0] = uid_list[i]
        if user_profile_results[i]['found']:
            profile_dict = user_profile_results[i]['_source']
            personal_info[1] = profile_dict['nick_name']
            personal_info[2] = profile_dict['user_location']
        if sensitive:
            sensitive_words = r_cluster.hget('sensitive_' + index_name, str(uid))
            if sensitive_words:
                sensitive_dict = json.loads(sensitive_words)
                personal_info[3] = sensitive_dict.keys() # sensitive words list
        else:
            try:
                personal_info[3] = user_profile_results[i]['_source']['fansnum']
            except:
                pass
        if user_bci_results[i]['found']:
            personal_info[4] = user_bci_results[i]['_source']['user_index']
        results.append(personal_info)
    return results


# show recommend in, sensitive user, date
# date = 20130901
def recommend_in_sensitive(date):
    date = date.replace('-','')
    results = r.hget('recommend_sensitive', date)
    if not results:
        return results # return '0'
    else:
        uid_list = json.loads(results)
    sensitive = 1
    return get_sensitive_user_detail(uid_list, date, sensitive)

# show top influence user recommend
def recommend_in_top_influence(date):
    date = date.replace('-','')
    results = r.hget('recommend_influence', date)
    if not results:
        return '0'
    else:
        uid_list = json.loads(results)
    sensitive = 0
    return get_sensitive_user_detail(uid_list, date, sensitive)


