# -*- coding: UTF-8 -*-
# push uid to redis

import sys
import json
import time
import redis

reload(sys)
sys.path.append('../../')
from time_utils import ts2datetime, datetime2ts
from global_utils import redis_ip
from global_utils import redis_activity
from parameter import RUN_TYPE, DAY, pre_ip, sen_pre_ip, pre_act,sen_pre_act
#from global_utils import ES_CLUSTER_FLOW2 as es_cluster

def scan_mapper():
    if RUN_TYPE:
        ts = datetime2ts(ts2datetime(time.time - DAY))
    else:
        ts = datetime2ts('2016-05-14')
    ts = str(ts)
    hash_name = sen_pre_ip + ts
    cursor = 0
    count = 0
    tb = time.time()

    while 1:
        re_scan = redis_ip.hscan(hash_name, cursor, count=1000)
        cursor = re_scan[0]
        ip_dict = re_scan[1]
        uid_list = ip_dict.keys()
        if uid_list:
            redis_ip.lpush('sensitive_ip_uid_list', json.dumps(uid_list))
            count += len(uid_list)
            ts = time.time()
            print '%s : %s' %(count, ts - tb)
            tb = ts
        if cursor == 0:
            print count
            break

if __name__ == "__main__":
    scan_mapper()
