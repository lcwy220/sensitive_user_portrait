# -*- coding:utf-8 -*-

# every 30 minutes reexecute this program

import sys
import time
import json
import redis
from elasticsearch import Elasticsearch
from text_attribute import compute_attribute
reload(sys)
sys.path.append('./../../')
from global_utils import R_RECOMMENTATION as r
from global_utils import es_sensitive_user_text as es_text
from time_utils import datetime2ts, ts2datetime

date = ts2datetime(time.time()).replace('-', '')
temp = r.hget('compute_now', date)
if temp:
    now_list = json.loads(temp)
    uid_list = []
    count = 0
    for item in now_list:
        uid_list.append(item[0])
    user_weibo_dict = dict()
    # extract user weibo text
    compute_attribute(user_weibo_dict)
    for i in range(now_list):
        uid = now_list[i][0]
        source = now_list[i][1]
        if source == '1':
            r.hset('identify_in_sensitive_'+str(date), uid, '3') # finish comoute
        else:
            r.hset('identify_in_influence_'+str(date), uid, '3')

    renow_list = json.loads(r.hget('compute_now', date))
    revise_set = set(renow_list) - set(now_list)
    if revise_set:
        r.hset('compute_now', date)
    else:
        r.hdel('compute_now', date)


