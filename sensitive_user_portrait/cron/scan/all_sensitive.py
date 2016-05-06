# -*-coding:utf-8-*-

#从flow4的redis_cluster中计算全网所有用户的敏感度，存储es

import sys
import numpy as np
import json
import time
import copy
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

reload(sys)
sys.path.append('./../../')
from global_utils import es_sensitive_history as es
from global_utils import redis_cluster as r_cluster
from global_utils import R_ADMIN as r_sensitive
from parameter import sensitive_score_dict, DAY
from global_utils import ES_SENSITIVE_INDEX, DOCTYPE_SENSITIVE_INDEX
from parameter import WEEK_TIME as WEEK
from parameter import MONTH_TIME as MONTH
from parameter import RUN_TYPE
from time_utils import ts2datetime, datetime2ts
from sensitive_history_mappings import mappings


def compute_week(item, now_ts):
    week_list = []
    for i in range(7):
        date_string = str(now_ts - i*DAY)
        week_list.append("sensitive_score_"+date_string)

    score_list = []
    for iter_key in week_list:
        if iter_key in set(item.keys()):
            score_list.append(item[iter_key])
    average = np.mean(score_list)
    var = np.var(score_list)
    total = sum(score_list)

    return average, var, total


def compute_month(item, now_ts):
    month_list = []
    for i in range(30):
        date_string = str(now_ts - i*DAY)
        month_list.append("sensitive_score_"+date_string)

    score_list = []
    for iter_key in month_list:
        if iter_key in set(item.keys()):
            score_list.append(item[iter_key])
    average = np.mean(score_list)
    var = np.var(score_list)
    total = sum(score_list)

    return average, var, total


def main():
    if RUN_TYPE:
        now_ts = time.time()-DAY # 前一天
        ts = str(datetime2ts(ts2datetime(now_ts)))
    else:
        ts = str(datetime2ts('2013-09-02'))
    now_ts = int(ts)
    print now_ts
    sensitive_string = "sensitive_" + ts
    date_string = ts
    update_sensitive_key = "sensitive_score_" + ts # 更新的键
    sensitive_dict_key = "sensitive_dict_" + ts
    sensitive_string_key = "sensitive_string_" + ts
    sensitive_day_change_key = "sensitive_" + ts +"_day_change"
    del_month = datetime2ts(ts2datetime(now_ts - MONTH))
    del_sensitive_key = "sensitive_score_"+str(del_month) # 要删除的键

    former_ts = int(ts) - DAY
    former_date = str(datetime2ts(ts2datetime(former_ts)))
    former_sensitive_key = "sensitive_score_" + former_date

    iter_count = 0
    bulk_action = []

    mappings(ES_SENSITIVE_INDEX)
    total_number = r_cluster.hlen(sensitive_string)
    scan_cursor = 0
    print total_number

    while 1:
        re_scan = r_cluster.hscan(sensitive_string, scan_cursor, count=1000)
        scan_cursor = re_scan[0]
        if len(re_scan[1]) != 0:
            sensitive_info = re_scan[1] # 字典形式，uid：sensitive_words_dict
            uid_list = sensitive_info.keys()
            sensitive_results = es.mget(index=ES_SENSITIVE_INDEX, doc_type=DOCTYPE_SENSITIVE_INDEX, body={"ids":uid_list})['docs']
            if sensitive_results:
                for item in sensitive_results:
                    uid = item['_id']
                    sensitive_words_dict = json.loads(sensitive_info[uid]) # json.loads
                    current_sensitive_score = 0
                    for k,v in sensitive_words_dict.iteritems():
                        tmp_stage = r_sensitive.hget("sensitive_words", k)
                        if tmp_stage:
                            tmp_stage = json.loads(tmp_stage)
                            current_sensitive_score += v*sensitive_score_dict[str(tmp_stage[0])]
                    if item['found']: # 之前存在相关信息
                        revise_item = item["_source"]
                        if del_sensitive_key in revise_item:
                            item.pop(del_sensitive_key)
                        revise_item['uid'] = uid
                        # 新更新的敏感度
                        revise_item[update_sensitive_key] = current_sensitive_score
                        revise_item['last_value'] = current_sensitive_score
                        # 新更新的敏感词
                        revise_item[sensitive_dict_key] = sensitive_info[uid]
                        # 新更新的string
                        revise_item[sensitive_string_key] = "&".join(sensitive_words_dict.keys())
                        # 当天和之前一天、一周和一月均值的差异
                        revise_item['sensitive_day_change'] = current_sensitive_score - revise_item.get(former_sensitive_key, 0)
                        revise_item['sensitive_week_change'] = current_sensitive_score - revise_item.get('sensitive_week_ave', 0)
                        revise_item['sensitive_month_change'] = current_sensitive_score - revise_item.get('sensitive_month_ave', 0)
                        # 更新后week、month的均值和方差
                        revise_item['sensitive_week_ave'], revise_item['sensitive_week_var'], revise_item['sensitive_week_sum'] = compute_week(revise_item, now_ts)
                        revise_item['senstiive_month_ave'], revise_item['sensitive_month_var'], revise_item['sensitive_month_sum'] = compute_month(revise_item, now_ts)

                    else:
                        revise_item = dict()
                        revise_item['uid'] = uid
                        revise_item[update_sensitive_key] = current_sensitive_score
                        revise_item['last_value'] = current_sensitive_score
                        revise_item[sensitive_dict_key] = sensitive_info[uid]
                        revise_item[sensitive_string_key] = "&".join(sensitive_words_dict.keys())
                        revise_item['sensitive_day_change'] = current_sensitive_score
                        revise_item['sensitive_week_change'] = current_sensitive_score
                        revise_item['sensitive_month_change'] = current_sensitive_score
                        revise_item['sensitive_week_ave'], revise_item['sensitive_week_var'], revise_item['sensitive_week_sum'] = compute_week(revise_item, now_ts)
                        revise_item['senstiive_month_ave'], revise_item['sensitive_month_var'], revise_item['sensitive_month_sum'] = compute_month(revise_item, now_ts)
                    action = {'index':{'_id': uid}}
                    bulk_action.extend([action, revise_item])
                    iter_count += 1
                    if iter_count % 1000 == 0:
                        es.bulk(bulk_action, index=ES_SENSITIVE_INDEX, doc_type=DOCTYPE_SENSITIVE_INDEX)
                        bulk_action = []
                        print iter_count
        if int(scan_cursor) == 0:
            break
    if bulk_action:
        es.bulk(bulk_action, index=ES_SENSITIVE_INDEX, doc_type=DOCTYPE_SENSITIVE_INDEX)

    print iter_count


    #######更新尚未完成的用户
    update_scan = scan(es, query={"query":{"filtered":{"filter":{"missing":{"field":update_sensitive_key}}}}}, index=ES_SENSITIVE_INDEX, doc_type=DOCTYPE_SENSITIVE_INDEX)
    iter_count = 0
    bulk_action = []

    while 1:
        try:
            tmp = update_scan.next()
            revise_item = tmp['_source']
            if del_sensitive_key in revise_item:
                revise_item.pop(del_sensitive_key)
            uid = tmp['_id']
            # 新更新的敏感度
            revise_item[update_sensitive_key] = 0
            revise_item['last_value'] = 0
            # 新更新的敏感词
            revise_item[sensitive_dict_key] = json.dumps({})
            # 新更新的string
            revise_item[sensitive_string_key] = ""
            # 当天和之前一天、一周和一月均值的差异
            revise_item['sensitive_day_change'] = 0 - revise_item.get(former_sensitive_key, 0)
            revise_item['sensitive_week_change'] = 0 - revise_item.get('sensitive_week_ave', 0)
            revise_item['sensitive_month_change'] = 0 - revise_item.get('sensitive_month_ave', 0)
            # 更新后week、month的均值和方差
            revise_item['sensitive_week_ave'], revise_item['sensitive_week_var'], revise_item['sensitive_week_sum'] = compute_week(revise_item, now_ts)
            revise_item['senstiive_month_ave'], revise_item['sensitive_month_var'], revise_item['sensitive_month_sum'] = compute_month(revise_item, now_ts)

            action = {'index':{'_id': uid}}
            bulk_action.extend([action, revise_item])
            iter_count += 1
            if iter_count % 1000 == 0:
                es.bulk(bulk_action, index=ES_SENSITIVE_INDEX, doc_type=DOCTYPE_SENSITIVE_INDEX)
                bulk_action = []
        except StopIteration:
            print "all done"
            if bulk_action:
                es.bulk(bulk_action, index=ES_SENSITIVE_INDEX, doc_type=DOCTYPE_SENSITIVE_INDEX)
            break
        except Exception, r:
            print Exception, r

    if bulk_action:
        es.bulk(bulk_action, index=ES_SENSITIVE_INDEX, doc_type=DOCTYPE_SENSITIVE_INDEX)

    print iter_count


if __name__ == "__main__":
    main()



