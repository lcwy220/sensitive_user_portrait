# -*- coding:utf-8 -*-
# 删除7天前的过期的redis数据：ip/activity/@;hashtag/sensitive_words;

import sys
import os
import redis
import time
reload(sys)
sys.path.append("../")
from time_utils import ts2datetime, datetime2ts, ts2date
from global_utils import redis_ip, redis_activity, redis_cluster
from global_utils import R_RECOMMENTATION as r
from global_utils import es_flow_text, flow_text_index_name_pre, flow_text_index_type, es_user_portrait, ES_CLUSTER_FLOW1
from parameter import EXPIRE_TIME, MONTH_TIME

def main():
    now_ts = time.time()
    delete_ts = datetime2ts(ts2datetime(now_ts-EXPIRE_TIME))  #待删除的时间戳
    delete_date = ts2datetime(now_ts-EXPIRE_TIME)
    del_day = ts2datetime(now_ts-MONTH_TIME)

    index_name = flow_text_index_name_pre + del_day
    exist_es = es_flow_text.indices.exists(index=index_name)
    if exist_es:
        es_flow_text.indices.delete(index=index_name)
    index_bci = "bci_" + del_day.replace('-', '')
    exist_bci = ES_CLUSTER_FLOW1.indices.exists(index=index_bci)
    if exist_bci:
        ES_CLUSTER_FLOW1.indices.delete(index=index_bci)


    #delete @
    redis_cluster.delete("at_"+str(delete_ts))
    redis_cluster.delete("sensitive_at_"+str(delete_ts))

    #delete ip
    redis_ip.delete('ip_'+str(delete_ts))
    redis_ip.delete('sensitive_ip_'+str(delete_ts))

    #delete activity
    redis_activity.delete('activity_'+str(delete_ts))
    redis_activity.delete('sensitive_activity_'+str(delete_ts))

    #delete hashtag
    redis_cluster.delete('hashtag_'+str(delete_ts))
    redis_cluster.delete('sensitive_hashtag_'+str(delete_ts))

    #delete sensitive words
    redis_cluster.delete('sensitive_'+str(delete_ts))

    #delete recommendation
    r.delete('recomment_'+str(delete_date))

if __name__ == "__main__":
    now_ts = time.time()
    current_path = os.getcwd()
    file_path_redis = os.path.join(current_path, 'delete_redis.py')
    print_log = "&".join([file_path_redis, "start", ts2datetime(now_ts)])
    print print_log

    now_datetime = datetime2ts(ts2datetime(now_ts))
    new_ip_number = r_cluster.hlen('new_ip_'+str(now_datetime))
    new_hashtag_number = r_cluster.hlen('hashtag_'+str(now_datetime))

    #if new_ip_number and new_hashtag_number: # flow2/flow4写入新数据,可以清楚8天前数据
    #    main()

    now_ts = time.time()
    print_log = "&".join([file_path_redis, "end", ts2datetime(now_ts)])
    print print_log


