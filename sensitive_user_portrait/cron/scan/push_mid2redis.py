# -*-coding:utf-8-*-
#将mid和更新的值push到redis里

import time
import sys
import redis
from elasticsearch import Elasticsearch
reload(sys)
sys.path.append('../../')
from global_utils import R_CLUSTER_FLOW1 as r
from global_utils import es_flow_text as es_text
from global_utils import redis_flow_text_mid as r_flow
from global_utils import flow_text_index_name_pre, flow_text_index_type
from parameter import DAY, RUN_TYPE

def main():
    scan_cursor = 0
    count = 0
    bulk_action = []
    number = r.scard('user_set')
    print number

    if RUN_TYPE:
        ts = time.time() - DAY
        date = ts2datetime(ts)
    else:
        date = '2013-09-05'
    index_name = flow_text_index_name_pre+date

    ts = time.time()
    while 1:
        re_scan = r.sscan("user_set", scan_cursor, count=3000)
        scan_cursor = re_scan[0]
        uid_list = re_scan[1] #具体数据
        if len(uid_list):
            for uid in uid_list:
                detail_dict = r.hgetall(uid)
                for k,v in detail_dict.iteritems():
                    update_dict = dict()
                    if "_origin_weibo_retweeted" in k and int(v):
                        mid = k.split('_')[0]
                        update_dict["retweeted"] = int(v)
                    elif "_origin_weibo_comment" in k and int(v):
                        mid = k.split('_')[0]
                        update_dict["comment"] = int(v)
                    else:
                        pass
                    if update_dict:
                        action = {"update": {"_id": mid}}
                        xdata = {"doc": update_dict}
                        bulk_action.extend([action, xdata])
                        count += 1
                        if count % 1000 == 0:
                            #print bulk_action
                            r_flow.lpush('update_mid_list', json.dumps(bulk_action))
                            bulk_action = []
                            tp = time.time()
                            print "%s cost %s" %(count, tp-ts)
                            ts = tp
        if int(scan_cursor) == 0:
            break

    if bulk_action:
        r_flow.lpush('update_mid_list', json.dumps(bulk_action))

    print count

if __name__ == "__main__":
    main()
