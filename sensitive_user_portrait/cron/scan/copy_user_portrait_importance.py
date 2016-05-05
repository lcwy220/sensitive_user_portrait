# -*-coding:utf-8-*-
# 从人物库user_portrait获得用户的重要度

import sys
import json
import time
import math
import numpy as np
from elasticsearch.helpers import scan

reload(sys)
sys.path.append('./../../')
from global_utils import es_user_portrait, portrait_index_name, portrait_index_type
from global_utils import ES_COPY_USER_PORTRAIT as es_cluster
from time_utils import ts2datetime, datetime2ts
from parameter import DAY
from parameter import MONTH_TIME as MONTH
from global_utils import COPY_USER_PORTRAIT_IMPORTANCE, COPY_USER_PORTRAIT_IMPORTANCE_TYPE
from parameter import RUN_TYPE, RUN_TEST_TIME

def compute_week(item, now_ts):
    week_list = []
    for i in range(7):
        date_string = str(now_ts - i*DAY)
        week_list.append("importance_"+date_string)

    score_list = []
    for iter_key in week_list:
        if iter_key in set(item.keys()):
            score_list.append(item[iter_key])
        #else:
        #    score_list.append(0)

    average = np.mean(score_list)
    var = np.var(score_list)
    total = sum(score_list)

    return average, var, total


def compute_month(item, now_ts):
    month_list = []
    for i in range(30):
        date_string = str(now_ts - i*DAY)
        month_list.append("importance_"+date_string)

    score_list = []
    for iter_key in month_list:
        if iter_key in set(item.keys()):
            score_list.append(item[iter_key])
        #else:
        #    score_list.append(0)

    average = np.mean(score_list)
    var = np.var(score_list)
    total = sum(score_list)

    return average, var, total


# 获取最大值
def get_max_index(term):
    query_body = {
        'query':{
            'match_all':{}
        },
        'size':1,
        'sort':[{term: {'order': 'desc'}}]
        }

    try:
        iter_max_value = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, \
                        body=query_body)['hits']['hits']
    except Exception, e:
        raise e
    iter_max = iter_max_value[0]['_source'][term]

    return iter_max


# normalize
def normal_index(index, max_index):
    normal_value = math.log((index / float(max_index)) * 9 + 1, 10) * 100
    return normal_value


def co_search(add_info, update_bci_key, former_bci_key, now_ts):
    uid_list = add_info.keys()
    evaluate_history_results = es_user_portrait.mget(index=COPY_USER_PORTRAIT_IMPORTANCE, doc_type=COPY_USER_PORTRAIT_IMPORTANCE_TYPE,body={'ids':uid_list})['docs']
    iter_count = 0
    bulk_action = []
    for uid in uid_list:
        item = evaluate_history_results[iter_count]
        if item['found']:
            user_history_item = item['_source']
            #更新新的字段
            user_history_item.update(add_info[uid])
            user_history_item['importance_day_change'] = user_history_item[update_bci_key] - user_history_item.get(former_bci_key, 0)
            user_history_item['importance_week_change'] = user_history_item[update_bci_key] - user_history_item.get('importance_week_ave', 0)
            user_history_item['importance_month_change'] = user_history_item[update_bci_key] - user_history_item.get('importance_month_ave', 0)
            user_history_item['importance_week_ave'], user_history_item['importance_week_var'], user_history_item['importance_week_sum'] = compute_week(user_history_item, now_ts)
            user_history_item['importance_month_ave'], user_history_item['importance_month_var'], user_history_item['importance_month_sum'] = compute_month(user_history_item, now_ts)
        else:
            user_history_item = dict()
            user_history_item.update(add_info[uid])
            user_history_item["uid"] = uid
            user_history_item.update(add_info[uid])
            user_history_item['importance_day_change'] = user_history_item[update_bci_key]
            user_history_item['importance_week_change'] = user_history_item[update_bci_key]
            user_history_item['importance_month_change'] = user_history_item[update_bci_key]
            user_history_item['importance_week_ave'], user_history_item['importance_week_var'], user_history_item['importance_week_sum'] = compute_week(user_history_item, now_ts)
            user_history_item['importance_month_ave'], user_history_item['importance_month_var'], user_history_item['importance_month_sum'] = compute_month(user_history_item, now_ts)
        iter_count += 1

        try:
            user_history_item.pop(del_bci_key)
        except:
            pass

        action = {'index':{'_id': uid}}
        bulk_action.extend([action, user_history_item])
    if bulk_action:
        es_cluster.bulk(bulk_action, index=COPY_USER_PORTRAIT_IMPORTANCE, doc_type=COPY_USER_PORTRAIT_IMPORTANCE_TYPE,timeout=600)
    print iter_count


def main():
    if RUN_TYPE:
        now_ts = time.time()-DAY # 前一天
        ts = str(datetime2ts(ts2datetime(now_ts)))
    else:
        ts = str(datetime2ts(RUN_TEST_TIME) - DAY)
    now_ts = int(ts)

    max_influence = get_max_index('importance')
    update_bci_key = "importance_" + ts # 更新的键
    del_month = str(datetime2ts(ts2datetime(now_ts - MONTH)))
    del_bci_key = "importance_" + del_month

    former_ts = now_ts - DAY
    former_date = str(datetime2ts(ts2datetime(former_ts)))
    former_bci_key = "importance_" + former_date

    s_re = scan(es_user_portrait, query={'query':{'match_all':{}}, 'size':1000},index=portrait_index_name, doc_type=portrait_index_type)
    bulk_action = []
    add_info = {}
    count = 0

    while 1:
        try:
            scan_re = s_re.next()['_source']
            count += 1
            uid = scan_re['uid']
            influence_value = scan_re['importance']
            normal_influence = normal_index(influence_value, max_influence)
            add_info[uid] = {update_bci_key: normal_influence, "domain": scan_re['domain'], "activity_geo": scan_re["activity_geo"], "hashtag": scan_re['hashtag'], "topic_string": scan_re["topic_string"]}

            if count % 1000 == 0:
                co_search(add_info, update_bci_key, former_bci_key, now_ts)
        except StopIteration:
            co_search(add_info, update_bci_key, former_bci_key, now_ts)
            break
        #except Exception, r:
        #    print Exception, r
        #    sys.exit(0)
    print count


if __name__ == "__main__":
    main()

