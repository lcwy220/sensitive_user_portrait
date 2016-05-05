# -*-coding:utf-8-*-
"""
放弃原先设想的采用redis cluster方案，而使用单台redis形式
"""
import os
import sys
import time
import redis
from redis import StrictRedis
reload(sys)
sys.path.append('../../')
from global_utils import R_CLUSTER_FLOW1 as r
from time_utils import ts2datetime
if __name__ == '__main__':
    ts = ts2datetime(time.time())

    r.flushdb()
    print "/cron/flow1/flush_db.py&end&%s" %ts

    
    path = "/home/ubuntu01/txt"
    file_list = os.listdir(path)
    for each in file_list:
        filename = each.split('.')[0]
        if filename.split('_')[-1] == 'yes':
            os.remove(path+'/'+each)
    print "/cron/flow1/del_file_yes.py&end&%s" %ts
