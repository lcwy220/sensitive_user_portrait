# -*- coding: UTF-8 -*-
# ip_2013-09-01

import sys
import json
import time
import redis
from mappings import mapping

reload(sys)
sys.path.append('../../')
from time_utils import ts2datetime, datetime2ts
from global_utils import redis_ip
from global_utils import redis_activity
from parameter import RUN_TYPE, DAY, ip_index_pre, ip_doc_type, sen_ip_index_pre, sen_ip_doc_type
from parameter import pre_ip, sen_pre_ip
from global_utils import ES_CLUSTER_FLOW2 as es_cluster

# ip
def scan_reducer():
    if RUN_TYPE:
        ts = datetime2ts(ts2datetime(time.time() - DAY))
    else:
        ts = datetime2ts('2016-05-14')
    date = ts2datetime(ts)
    ts = str(ts)
    hash_name = sen_pre_ip + ts
    #index_name = ip_index_pre + date
    sen_index_name = sen_ip_index_pre + date
    mapping(sen_index_name, sen_ip_doc_type)
    count = 0
    bulk_action = []
    tb = time.time()

    while 1:
        tmp_list = redis_ip.rpop('sensitive_ip_uid_list')
        if tmp_list:
            uid_list = json.loads(tmp_list)
            ip_dict = redis_ip.hmget(hash_name, uid_list)
            for i in range(len(uid_list)):
                save_dict = dict()
                uid = uid_list[i]
                save_dict['uid'] = uid_list[i]
                save_dict['sensitive_ip_dict'] = ip_dict[i]
                bulk_action.extend([{'index':{'_id':uid}}, save_dict])
            es_cluster.bulk(bulk_action, index=sen_index_name, doc_type=sen_ip_doc_type)
            bulk_action = []
            count += len(uid_list)
            te = time.time()
            if RUN_TYPE == 0:
                print '%s sec scan %s count user' % (te-tb, count)
            tb = te
        else:
           print count
           break

    #redis_ip.delete(hash_name)

if __name__ == "__main__":
    scan_reducer()
