# -*- coding: UTF-8 -*-
import IP
import sys
import json
import time
import math
import numpy as np
from save_utils import save_group_results
from config import activeness_weight_dict, importance_weight_dict,\
                   domain_weight_dict, topic_weight_dict, tightness_weight_dict
from topic_lda import topic_lda_main
reload(sys)
sys.path.append('../../')
from global_utils import es_user_portrait as es
from global_utils import R_GROUP as r
from global_utils import group_analysis_queue_name
from global_utils import es_user_portrait, portrait_index_name, portrait_index_type ,\
                         es_group_result, group_index_name, group_index_type ,\
                         es_retweet, retweet_index_name_pre, retweet_index_type ,\
                         be_retweet_index_name_pre, be_retweet_index_type ,\
                         es_comment, comment_index_name_pre, comment_index_type ,\
                         be_comment_index_name_pre, be_comment_index_type ,\
                         es_flow_text, flow_text_index_name_pre, flow_text_index_type,\
                         es_copy_portrait, copy_portrait_index_name, copy_portrait_index_type,\
                         es_user_profile, profile_index_name, profile_index_type
from global_utils import ES_COPY_USER_PORTRAIT, COPY_USER_PORTRAIT_INFLUENCE, COPY_USER_PORTRAIT_INFLUENCE_TYPE,\
        COPY_USER_PORTRAIT_ACTIVENESS, COPY_USER_PORTRAIT_ACTIVENESS_TYPE
from global_utils import redis_cluster, redis_activity
from global_utils import ES_CLUSTER_FLOW1 as es_cluster
from global_config import R_BEGIN_TIME
from parameter import ACTIVITY_GEO_TOP, MAX_VALUE, DAY, HIS_BINS_COUNT, GROUP_ACTIVITY_TIME_THRESHOLD, \
        GROUP_ACTIVITY_TIME_DESCRIPTION_DICT, GROUP_INFLUENCE_FILTER_LOW_THRESHOLD,\
        GROUP_ITER_COUNT, GROUP_INFLUENCE_FILTER_RANK_RATIO, GROUP_SOCIAL_OUT_COUNT,\
        GROUP_AVE_ACTIVENESS_RANK_THRESHOLD, GROUP_AVE_INFLUENCE_RANK_THRESHOLD,\
        GROUP_AVE_ACTIVENESS_RANK_DESCRIPTION, GROUP_AVE_INFLUENCE_RANK_DESCRIPTION,\
        GROUP_AVE_IMPORTANCE_RANK_DESCRIPTION, GROUP_AVE_IMPORTANCE_RANK_THRESHOLD,\
        IDENTIFY_ATTRIBUTE_LIST, GROUP_DENSITY_THRESHOLD, GROUP_DENSITY_DESCRIPTION,\
        GROUP_SENTIMENT_LIST, GROUP_NEGATIVE_SENTIMENT, GROUP_KEYWORD_COUNT,\
        GROUP_HASHTAG_COUNT, GROUP_SENTIMENT_WORD_COUNT, TOPIC_MODEL_COUNT, \
        GROUP_INDEX_RANK_RATIO_DICT, GROUP_SENSITIVE_WORDS_COUNT
from parameter import RUN_TYPE, RUN_TEST_TIME
from time_utils import ts2datetime, datetime2ts, datetimestr2ts, ts2date


r_begin_ts = datetime2ts(R_BEGIN_TIME)

#use to merge dict
#input: dict1, dict2, dict3...
#output: merge dict
def union_dict(*objs):
    _keys = set(sum([obj.keys() for obj in objs], []))
    _total = {}
    for _key in _keys:
        _total[_key] = sum([int(obj.get(_key, 0)) for obj in objs])
    return _total

#use to merge dict list
#input: dict_list
#ouput: merge_dict
def union_dict_list(objs):
    _keys = set(sum([obj.keys() for obj in objs], []))
    _total = {}
    for _key in _keys:
        _total[_key] = sum([int(obj.get(_key, 0)) for obj in objs])

    return _total

#use to merge dict list and filter by uid_list
#input: dict_list
#output: meige_dict
def filter_union_dict(objs, filter_uid_list, mark):
    _keys = set(sum([obj.keys() for obj in objs], []))
    if mark == 'in&out':
        _in_total = {}
        _in_keys = _keys & set(filter_uid_list)
        for _key in _in_keys:
            _in_total[_key] = sum([int(obj.get(_key,0)) for obj in objs])
        _out_total = {} 
        _out_keys = _keys - set(filter_uid_list)
        for _key in _out_keys:
            _out_total[_key] = sum([int(obj.get(_key, 0)) for obj in objs])       
        return _in_total, _out_total
    elif mark == 'out':
        _out_total = {}
        _out_keys = _keys - set(filter_uid_list)
        for _key in _out_keys:
            _out_total[_key] = sum([int(obj.get(_key, 0)) for obj in objs])
        return _out_total

# compute index rank like importance/activeness/influence rank
# input: index_value and index_type
# output: index_rank
def get_index_rank(index_value, index_name):
    result = 0
    query_body = {
            'query':{
                'range':{
                    index_name:{
                        'from':index_value,
                        'to': MAX_VALUE
                        }
                    }
                }
            }
    index_rank = es_user_portrait.count(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)
    if index_rank['_shards']['successful'] != 0:
       result = index_rank['count']
    else:
        print 'es index rank error'
        result = 0
    return result


#compute attr from es_user_portrait
#version: 16-01-22
#input: uid_list
#output: 
def get_attr_portrait(uid_list, submit_user):
    results = {}
    #init some dict
    gender_ratio = dict()
    verified_ratio = dict()
    online_pattern_ratio = dict()
    domain_ratio = dict()
    politics_ratio = dict()
    topic_ratio = dict()
    keyword_ratio = dict()
    sensitive_hashtag_ratio = dict()
    hashtag_ratio = dict()
    sensitive_words_ratio = dict()
    character_dict = {'character_sentiment':{}, 'character_text':{}}
    activity_geo_distribution_date = dict() # {'date1':{geo1:person_count, geo2:person_count}, 'date2':{geo1:person_count,..}, ..} # one month
    activity_geo_vary = dict() # {'geo2geo': count, ...}  geo2geo='activity_geo1&activity_geo2'
    main_start_geo = dict()
    main_end_geo = dict()
    vary_detail_geo = dict()
    importance_list = []
    influence_list = []
    influence_rank_ratio_dis = {}
    sensitive_list = []
    sensitive_rank_ratio_dis = {}
    activeness_list = []
    activeness_rank_ratio_dis = {}
    sentiment_dict_list = []
    tag_dict = {}
    #get now date to iter activity geo
    #run_type
    if RUN_TYPE == 1:
        now_ts = int(time.time())
    else:
        now_ts = datetime2ts(RUN_TEST_TIME)
    now_date_ts = datetime2ts(ts2datetime(now_ts))
    #split uid_list to bulk action
    iter_count = 0
    all_user_count = len(uid_list)
    while iter_count < all_user_count:
        iter_uid_list = uid_list[iter_count: iter_count + GROUP_ITER_COUNT]
        try:
            iter_user_dict_list = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, \
                body={'ids':iter_uid_list})['docs']
        except:
            iter_user_dict_list = []

        for user_dict in iter_user_dict_list:
            uid = user_dict['_id']
            source = user_dict['_source']
            #attr1: gender ratio:
            gender = source['gender']
            try:
                gender_ratio[gender] += 1
            except:
                gender_ratio[gender] = 1
            #attr2: verified ratio
            verified = source['verified']
            try:
                verified_ratio[verified] += 1
            except:
                verified_ratio[verified] = 1
            #attr3: online pattern
            online_pattern = source['online_pattern']
            online_pattern = json.loads(online_pattern)
            for pattern in online_pattern:
                try:
                    online_pattern_ratio[pattern] += 1
                except:
                    online_pattern_ratio[pattern] = 1

            # attr 3.8 sensitive_words
            sensitive_words_dic_ = json.loads(source['sensitive_words_dict'])
            for w, c in sensitive_words_dic_.iteritems():
                if w != '':
                    try:
                        sensitive_words_ratio[w] += c
                    except:
                        sensitive_words_ratio[w] = c

            # attr3.9: politics
            politics = source['politics']
            try:
                politics_ratio[politics] += 1
            except:
                politics_ratio[politics] = 1
            #attr4: domain
            domain = source['domain']
            try:
                domain_ratio[domain] += 1
            except:
                domain_ratio[domain] = 1
            #attr5: topic
            topic_string = source['topic_string']
            topic_list = topic_string.split('&')
            for topic in topic_list:
                try:
                    topic_ratio[topic] += 1
                except:
                    topic_ratio[topic] = 1
            #attr6: keywords_string
            keywords_string = source['keywords_string']
            keywords_list = keywords_string.split('&')
            for keyword in keywords_list:
                try:
                    keyword_ratio[keyword] += 1
                except:
                    keyword_ratio[keyword] = 1
            # attr 6.9: sensitive_hashtag
            sensitive_hashtag_dic_ = json.loads(source['sensitive_hashtag_dict'])
            for k, v in sensitive_hashtag_dic_.iteritems():
                try:
                    sensitive_hashtag_ratio[k] += v
                except:
                    sensitive_hashtag_ratio[k] = v

            #attr7: hashtag
            hashtag_string = source['hashtag_string']
            hashtag_list = hashtag_string.split('&')
            for hashtag in hashtag_list:
                if hashtag != '':
                    try:
                        hashtag_ratio[hashtag] += 1
                    except:
                        hashtag_ratio[hashtag] = 1
            #attr8: activity_geo_dict---distribution by date
            user_activity_geo = {}
            activity_geo_dict_list = json.loads(source['activity_geo_dict'])
            activity_geo_date_count = len(activity_geo_dict_list)
            iter_ts = now_date_ts - activity_geo_date_count * DAY
            user_date_main_list = []
            for i in range(0, activity_geo_date_count):
                date_item = activity_geo_dict_list[i]
                if iter_ts in activity_geo_distribution_date:
                    activity_geo_distribution_date[iter_ts] = union_dict_list([activity_geo_distribution_date[iter_ts], date_item])
                else:
                    activity_geo_distribution_date[iter_ts] = date_item
                #use to get activity_geo vary
                sort_date_item = sorted(date_item.items(), key=lambda x:x[1], reverse=True)
                if date_item != {}:
                    main_date_city = sort_date_item[0][0]
                    try:
                        last_user_date_main_item = user_date_main_list[-1][0]
                    except:
                        last_user_date_main_item = ''
                    if main_date_city != last_user_date_main_item:
                        user_date_main_list.append([main_date_city, iter_ts])

                iter_ts += DAY
            #attr8: activity_geo_dict---location vary
            if len(user_date_main_list) > 1:
                for i in range(1, len(user_date_main_list)):
                    vary_city = [geo_ts_item[0] for geo_ts_item in user_date_main_list[i-1:i+1]]
                    vary_ts = [geo_ts_item[1] for geo_ts_item in user_date_main_list[i-1:i+1]]
                    vary_item = '&'.join(vary_city)
                    #vary_item = '&'.join(user_date_main_list[i-1:i+1])
                    #get activity geo vary for vary table and map
                    try:
                        activity_geo_vary[vary_item] += 1
                    except:
                        activity_geo_vary[vary_item] = 1
                    #get main start geo
                    try:
                        main_start_geo[vary_city[0]] += 1
                    except:
                        main_start_geo[vary_city[0]] = 1
                    #get main end geo
                    try:
                        main_end_geo[vary_city[1]] += 1
                    except:
                        main_end_geo[vary_city[1]] = 1
                    #get vary detail geo
                    try:
                        vary_detail_geo[vary_item].append([uid, vary_ts[0], vary_ts[1]])
                    except:
                        vary_detail_geo[vary_item] = [[uid, vary_ts[0], vary_ts[1]]]
            # attr 8.9: sensitive distribution
            sensitive = source['sensitive']
            sensitive_rank = get_index_rank(sensitive, 'sensitive')
            sensitive_list.append(sensitive_rank)
            #attr9: influence distribution
            influence = source['influence']
            influence_rank = get_index_rank(influence, 'influence')
            influence_list.append(influence_rank) 
            #attr10: importance distribution
            importance = source['importance']
            importance_rank = get_index_rank(importance, 'importance')
            importance_list.append(importance_rank)
            #attr11: activeness distribution
            activeness = source['activeness']
            activeness_rank = get_index_rank(activeness, 'activeness')
            activeness_list.append(activeness_rank)
            #attr12: tag
            try:
                portrait_tag_string = source[submit_user + '-tag']
            except:
                portrait_tag_string = ''
            if portrait_tag_string != '':
                portrait_tag_list = portrait_tag_string.split('&')
                for portrait_tag_item in portrait_tag_list:
                    tag_dict_key = ':'.join(portrait_tag_item.split('-'))
                    try:
                        tag_dict[portrait_tag_item] += 1
                    except:
                        tag_dict[portrait_tag_item] = 1

        iter_count += GROUP_ITER_COUNT
    # importance ditribution
    p, t = np.histogram(importance_list, bins=HIS_BINS_COUNT, normed=False)
    results['importance_his'] = json.dumps([p.tolist(), [int(item) for item in t.tolist()]])
    p, t = np.histogram(influence_list, bins=HIS_BINS_COUNT, normed=False)
    results['influence_his'] = json.dumps([p.tolist(), [int(item) for item in t.tolist()]])
    p, t = np.histogram(sensitive_list, bins=HIS_BINS_COUNT, normed=False)
    results['sensitive_his'] = json.dumps([p.tolist(), [int(item) for item in t.tolist()]])
    p, t = np.histogram(activeness_list, bins=HIS_BINS_COUNT ,normed=False)
    results['activeness_his'] = json.dumps([p.tolist(), [int(item) for item in t.tolist()]])
    # ave activeness rank
    ave_activeness_rank = float(sum(activeness_list)) / len(activeness_list)
    try:
        all_user_count = es_user_portrait.count(index=portrait_index_name, doc_type=portrait_index_type,\
            body={'query':{'match_all':{}}})['count']
    except Exception, e:
        raise e
    if ave_activeness_rank <= GROUP_AVE_ACTIVENESS_RANK_THRESHOLD[0] * all_user_count:
        results['activeness_description'] = GROUP_AVE_ACTIVENESS_RANK_DESCRIPTION['0']
        results['activeness_star'] = 5
    elif ave_activeness_rank > GROUP_AVE_ACTIVENESS_RANK_THRESHOLD[1] * all_user_count:
        results['activeness_description'] = GROUP_AVE_ACTIVENESS_RANK_DESCRIPTION['2']
        results['activeness_star'] = 1
    else:
        results['activeness_description'] = GROUP_AVE_ACTIVENESS_RANK_DESCRIPTION['1']
        results['activeness_star'] = 3
    # ave influence rank
    ave_influence_rank = float(sum(influence_list) / len(influence_list))
    if ave_influence_rank <= GROUP_AVE_INFLUENCE_RANK_THRESHOLD[0] * all_user_count:
        results['influence_description'] = GROUP_AVE_INFLUENCE_RANK_DESCRIPTION['0']
        results['influence_star'] = 5
    elif ave_influence_rank > GROUP_AVE_INFLUENCE_RANK_THRESHOLD[1] * all_user_count:
        results['influence_description'] = GROUP_AVE_INFLUENCE_RANK_DESCRIPTION['2']
        results['influence_star'] = 1
    else:
        results['influence_description'] = GROUP_AVE_INFLUENCE_RANK_DESCRIPTION['1']
        results['influence_star'] = 3
    #ave importance rank
    ave_importance_rank = float(sum(importance_list) / len(importance_list))
    if ave_importance_rank <= GROUP_AVE_IMPORTANCE_RANK_THRESHOLD[0] * all_user_count:
        results['importance_description'] = GROUP_AVE_IMPORTANCE_RANK_DESCRIPTION['0']
        results['importance_star'] = 5
    elif ave_importance_rank > GROUP_AVE_IMPORTANCE_RANK_THRESHOLD[1] * all_user_count:
        results['importance_description'] = GROUP_AVE_IMPORTANCE_RANK_DESCRIPTION['2']
        results['importance_star'] = 1
    else:
        results['importance_description'] = GROUP_AVE_IMPORTANCE_RANK_DESCRIPTION['1']
        results['importance_star'] = 3
    # get result dict
    tag_vector_result = {}
    results['gender'] = json.dumps(gender_ratio)
    results['verified'] = json.dumps(verified_ratio)
    results['user_tag'] = json.dumps(tag_dict)
    results['online_pattern'] = json.dumps(online_pattern)
    results['character'] = json.dumps(character_dict)
    #tag vector---main domain
    sort_domain_ratio = sorted(domain_ratio.items(), key=lambda x:x[1], reverse=True)
    main_domain = sort_domain_ratio[0][0]
    tag_vector_result['domain'] = [u'主要领域', main_domain]
    results['domain'] = json.dumps(sort_domain_ratio)
    #tag vector---main topic
    sort_topic_ratio = sorted(topic_ratio.items(), key=lambda x:x[1], reverse=True)
    sort_politics_ratio = sorted(politics_ratio.items(), key=lambda x:x[1], reverse=True)
    main_topic = sort_topic_ratio[0][0]
    tag_vector_result['topic'] = [u'主要话题', main_topic]
    results['topic'] = json.dumps(sort_topic_ratio)
    results['politics'] = json.dumps(sort_politics_ratio)
    results['activity_geo_distribution'] = json.dumps(activity_geo_distribution_date)
    results['activity_geo_vary'] = json.dumps(activity_geo_vary)
    results['main_start_geo'] = json.dumps(main_start_geo)
    results['main_end_geo'] = json.dumps(main_end_geo)
    results['vary_detail_geo'] = json.dumps(vary_detail_geo)
    #main activity geo
    all_activity_geo = union_dict_list(activity_geo_distribution_date.values())
    sort_all_activity_geo = sorted(all_activity_geo.items(), key=lambda x:x[1], reverse=True)
    main_activity_geo = sort_all_activity_geo[0][0]
    #tag vector---main activity geo
    tag_vector_result['activity_geo'] = [u'主要分布城市', main_activity_geo]
    sort_keyword_ratio = sorted(keyword_ratio.items(), key=lambda x:x[1], reverse=True)[:GROUP_KEYWORD_COUNT]
    results['keywords'] = json.dumps(sort_keyword_ratio)
    #tag vector---main hashtag
    sort_sensi_hashtag_dict = sorted(sensitive_hashtag_ratio.items(), key=lambda x:x[1], reverse=True)[:GROUP_HASHTAG_COUNT]
    sort_hashtag_dict = sorted(hashtag_ratio.items(), key=lambda x:x[1], reverse=True)[:GROUP_HASHTAG_COUNT]
    results['hashtag'] = json.dumps(sort_hashtag_dict)
    results['sensitive_hashtag'] = json.dumps(sort_sensi_hashtag_dict)
    sort_sensitive_words_ratio = sorted(sensitive_words_ratio.items(), key=lambda x:x[1], reverse=True)[:GROUP_SENSITIVE_WORDS_COUNT]
    results['sensitive_words'] = json.dumps(sort_sensitive_words_ratio)

    if len(sort_hashtag_dict) != 0:
        tag_vector_result['hashtag'] = [u'hashtag', sort_hashtag_dict[0][0]]
    else:
        tag_vector_result['hashtag'] = [u'hashtag', '暂无']
    return results, tag_vector_result

def get_index_rank_ratio(rank, all_count):
    result = 0
    ratio = float(rank) / all_count
    if ratio < GROUP_INDEX_RANK_RATIO_DICT[1]:
        result = GROUP_INDEX_RANK_RATIO_DICT[1]
    elif ratio > GROUP_INDEX_RANK_RATIO_DICT[4]:
        result = GROUP_INDEX_RANK_RATIO_DICT[5]
    elif ratio > GROUP_INDEX_RANK_RATIO_DICT[1] and ratio <= GROUP_INDEX_RANK_RATIO_DICT[2]:
        result = GROUP_INDEX_RANK_RATIO_DICT[2]
    elif ratio > GROUP_INDEX_RANK_RATIO_DICT[2] and ratio <= GROUP_INDEX_RANK_RATIO_DICT[3]:
        result = GROUP_INDEX_RANK_RATIO_DICT[3]
    else:
        result = GROUP_INDEX_RANK_RATIO_DICT[4]
    
    return result


#use to get db number for retweet/be_retweet/comment/be_comment
#input: timestamp
#output: db_number
def get_db_num(timestamp):
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    db_number = (((date_ts - r_begin_ts) / DAY) / 7) % 2 + 1
    #run_type
    if RUN_TYPE == 0:
        db_number = 1
    return db_number

#use to get group social attribute
#write in version: 16-01-23
#input: uid_list
#output: group social attribute
def get_attr_social(uid_list, uid2uname):
    result = {}
    #step1: get db number
    timestamp = int(time.time())
    db_num = get_db_num(timestamp)
    retweet_index_name = retweet_index_name_pre + str(db_num)
    be_retweet_index_name = be_retweet_index_name_pre + str(db_num)
    comment_index_name = comment_index_name_pre + str(db_num)
    be_comment_index_name = be_comment_index_name_pre + str(db_num)
    #step2: split uid list to iter mget
    iter_count = 0
    all_user_count = len(uid_list)
    in_stat_results = dict()
    out_stat_result = dict()
    all_in_record = []
    all_out_record = []
    all_out_user_count = 0
    all_out_in_usr_count = 0
    while iter_count < all_user_count:
        iter_uid_list = uid_list[iter_count:iter_count+GROUP_ITER_COUNT]
        #step3:mget retweet
        retweet_result = es_retweet.mget(index=retweet_index_name, doc_type=retweet_index_type, body={'ids':iter_uid_list})['docs']
        retweet_dict = {} #{uid1: {ruid1:count1, ruid2:count2}, uid2:{},...}
        for item in retweet_result:
            uid = item['_id']
            #tesit for error es
            if item['found'] == True:
                retweet_dict[uid] = json.loads(item['_source']['uid_retweet'])
            else:
                retweet_dict[uid] = {}

        #step4:mget comment
        comment_result = es_comment.mget(index=comment_index_name, doc_type=comment_index_type, body={'ids':iter_uid_list})['docs']
        comment_dict = {} #{uid1:{ruid1:count1, ruid2:count2},...}
        for item in comment_result:
            uid = item['_id']
            if item['found'] == True:
                comment_dict[uid] = json.loads(item['_source']['uid_comment'])
            else:
                comment_dict[uid] = {}

        #step5:mget be_retweet
        be_retweet_result = es_comment.mget(index=be_retweet_index_name, doc_type=be_retweet_index_type, body={'ids':iter_uid_list})['docs']
        be_retweet_dict = dict() #{uid1: {uid_be_retweet dict}, uid2:{},...}
        for item in be_retweet_result:
            uid = item['_id']
            #test for error es
            if item['found'] == True:
                be_retweet_dict[uid] = json.loads(item['_source']['uid_be_retweet'])
            else:
                be_retweet_dict[uid] = {}

        #step6:mget be_comment
        be_comment_result = es_comment.mget(index=be_comment_index_name, doc_type=be_comment_index_type, body={'ids':iter_uid_list})['docs']
        be_comment_dict = dict() #{uid1:{uid_be_comment dict}, uid2:{},...}
        for item in be_comment_result:
            uid = item['_id']
            #test for error es
            if item['found'] == True:
                be_comment_dict[uid] = json.loads(item['_source']['uid_be_comment'])
            else:
                be_comment_dict[uid] = {}

        #step7:union retweet&comment, be_retweet&be_comment
        for iter_uid in iter_uid_list:
            user_retweet_result = retweet_dict[iter_uid]
            user_comment_result = comment_dict[iter_uid]
            filter_in_dict, filter_out_dict = filter_union_dict([user_retweet_result, user_comment_result], uid_list, 'in&out')
            #step8: record the retweet/coment relaton in group uid 
            uid_in_record = [[iter_uid, ruid, filter_in_dict[ruid], uid2uname[iter_uid], uid2uname[ruid]] for ruid in filter_in_dict if iter_uid != ruid]
            all_in_record.extend(uid_in_record)  # [[uid1, ruid1, count1],[uid1,ruid2,count2],[uid2,ruid2,count3],...]
            #step9: record the retweet/comment/be_retweet/be_comment relation out group uid
            user_be_retweet_result = be_retweet_dict[iter_uid]
            user_be_comment_result = be_comment_dict[iter_uid]
            filter_out_dict = filter_union_dict([filter_out_dict, user_be_retweet_result, user_be_comment_result], uid_list, 'out')
            #step10: filter out user who is in user_portrait
            uid_out_record = []
            if len(filter_out_dict):
                out_in_user_portrait = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, body={'ids':filter_out_dict.keys()}, _source=False, fields=['influence'])['docs']
                for out_in_item in out_in_user_portrait:
                    ruid = out_in_item['_id']
                    if out_in_item['found'] == True and ruid != iter_uid:
                        influence = out_in_item['fields']['influence'][0]
                        uid_out_record.append([iter_uid, ruid, filter_out_dict[ruid], influence, uid2uname[iter_uid]])
            all_out_record.extend(uid_out_record) #[[uid1, ruid1,count1],[uid1,ruid2,count2],[uid2,ruid2,count3],...]
        iter_count += GROUP_ITER_COUNT
    #step11 sort interaction in group by retweet&comment count
    sort_in_record = sorted(all_in_record, key=lambda x:x[2], reverse=True)
    result['social_in_record'] = json.dumps(sort_in_record)
    #step12: sort interaction out group by influence
    sort_out_record = sorted(all_out_record, key=lambda x:x[3], reverse=True)[:GROUP_SOCIAL_OUT_COUNT]
    #get social out user uname
    sort_out_record_out_user = [item[1] for item in sort_out_record]
    if len(sort_out_record_out_user):
        user_profile_result = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type, body={'ids': sort_out_record_out_user}, _source=False, fields=['nick_name'])['docs']
    else:
        user_profile_result = []

    out_uid2uname = {}
    for user_profile_item in user_profile_result:
        uid = user_profile_item['_id']
        if user_profile_item['found'] == True:
            out_uid2uname[uid] = user_profile_item['fields']['nick_name'][0]
        else:
            out_uid2uname[uid] = 'unknown'
    sort_out_record = [[item[0], item[1], item[2], item[3], item[4], out_uid2uname[item[1]]] for item in sort_out_record]
    result['social_out_record'] = json.dumps(sort_out_record)
    #step13: compute interaction index---in group
    in_inter_edge_count = len(sort_in_record)
    result['in_density'] = float(in_inter_edge_count) / (len(uid_list) * (len(uid_list) - 1))
    #density description
    if result['in_density'] <= GROUP_DENSITY_THRESHOLD[0]:
        result['density_description'] = GROUP_DENSITY_DESCRIPTION['0']
        result['density_star'] = 1
    elif result['in_density'] > GROUP_DENSITY_THRESHOLD[-1]:
        result['density_description'] = GROUP_DENSITY_DESCRIPTION['2']
        result['density_star'] = 5
    else:
        result['density_description'] = GROUP_DENSITY_DESCRIPTION['1']
        result['density_star'] = 3
    in_inter_weibo_count = sum([item[2] for item in sort_in_record])
    result['in_inter_weibo_ratio'] = float(in_inter_weibo_count) / len(uid_list)
    in_inter_user_count = len(set([item[0] for item in sort_in_record]) | set([item[1] for item in sort_in_record]))
    result['in_inter_user_ratio'] = float(in_inter_user_count) / len(uid_list)
    #step14: compute interaction index---out group
    in_out_inter_user_count = len(set([item[0] for item in all_out_record])) # who is in user_portrait
    result['out_inter_user_ratio'] = float(in_out_inter_user_count) / len(uid_list) # the ratio of uid in group who interact with out group
    out_outer_weibo_count = sum([item[2] for item in all_out_record])
    result['out_inter_weibo_ratio'] = float(out_outer_weibo_count) / len(uid_list)
    #step15:  @ network---result [[uid1, @uname, count], [uid2, @uname, count],...]
    now_ts = int(time.time())
    now_date_ts = datetime2ts(ts2datetime(now_ts))
    union_mention_dict = dict()
    for i in range(7, 0, -1):
        iter_ts = now_date_ts - i*DAY
        result_string_list = redis_cluster.hmget('at_'+str(iter_ts), uid_list)
        count = 0
        for uid in uid_list:
            result_dict = result_string_list[count]
            if result_dict:
                result_dict = json.loads(result_dict)
            else:
                result_dict = {}
            try:
                union_mention_dict[uid] = union_dict(union_mention_dict[uid], result_dict)
            except:
                union_mention_dict[uid] = union_dict({}, result_dict)

            count += 1
    #make [[uid1, @uname, count], [uid2, @uname, count], ...]
    mention_list = []
    for uid in union_mention_dict:
        uid_mention_dict = union_mention_dict[uid]
        uname = uid2uname[uid]
        if uid_mention_dict:
            uid_mention_list = [[uid, uname, at_uname, uid_mention_dict[at_uname]] for at_uname in uid_mention_dict]
        else:
            uid_mention_list = []
        mention_list.extend(uid_mention_list)
    sort_mention_list = sorted(mention_list, key=lambda x:x[3], reverse=True)
    result['mention'] = sort_mention_list
    return result

#use to filter uid_list by influence_threshold
#input: uid_list
#output: new_uid_list
#two scen---1)influence threshold 2) influence rank ratio
def influence_user_filter(uid_list):
    new_uid_list = []
    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                            {'terms': {'uid': uid_list}},
                            {'range':{'influence': {'gte': GROUP_INFLUENCE_FILTER_LOW_THRESHOLD, 'lt': MAX_VALUE}}}
                            ]
                        }
                    }
                }
            }
        }
    try:
        threshold_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type,\
                                    body=query_body, _source=False, fileds=['influence'])['hits']['hits']
    except:
        threshold_result = []
    if threshold_result != []:
        #scen1: filter by threshold
        for item in threshold_result:
            new_uid_list.append(item['_id'])
    else:
        #scen2: filter by influence rank ratio
        try:
            threshold_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type,\
                                    body={'ids':uid_list}, _source=False, fileds=['influence'])['hits']['hits']
        except:
            threshold_result = []
        uid_influence_dict = {}
        for item in threshold_result:
            if item['found']==True:
                uid_influence_dict[item['_id']] = item['fields']['influence'][0]
        sort_uid_influence_list = sorted(uid_influence_dict, key=lambda x:x[1])
        filter_count = int(len(sort_uid_influence_list) * GROUP_INFLUENCE_FILTER_RANK_RATIO)
        after_filter_uid_influence_list = sort_uid_influence_list[filter_count:]
        new_uid_list = [item[0] for item in after_filter_uid_influence_list]

    return new_uid_list


#use to get influence user
#input: uid
#output: results
def get_influence_user(uid_list):
    results = {}
    #step0: filter uid_list by influence_threshold
    #uid_list = influence_user_filter(uid_list)
    #step1:get be_retweet_uid/be_comment
    now_ts = int(time.time())
    db_number = get_db_num(now_ts)
    be_retweet_index_name = be_retweet_index_name_pre + str(db_number)
    be_comment_index_name = be_comment_index_name_pre + str(db_number)
    try:
       be_retweet_result = es_retweet.mget(index=be_retweet_index_name, doc_type=be_retweet_index_type,\
                                            body={'ids':uid_list})['docs']
    except:
        be_retweet_result = []
    be_retweet_dict_list = []
    for item in be_retweet_result:
        #test for error es
        try:
            if item['found'] == True:
                be_retweet_dict_list.append(json.loads(item['_source']['uid_be_retweet']))
        except:
            pass
    union_be_retweet_dict = union_dict_list(be_retweet_dict_list)
    try:
        be_comment_result = es_comment.mget(index=be_comment_index_name, doc_type=be_comment_index_type ,\
                                            body={'ids':uid_list})['docs']
    except:
        be_comment_result = []
    be_comment_dict_list = []
    for item in be_comment_result:
        #test for error es
        try:
            if item['found'] == True:
                be_comment_dict_list.append(json.loads(item['_source']['uid_be_comment']))
        except:
            pass
    union_be_comment_dict = union_dict_list(be_comment_dict_list)
    #get all influence user
    all_influence_user_dict = union_dict_list([union_be_retweet_dict, union_be_comment_dict])
    #filter uid list
    for uid in uid_list:
        try:
            all_influence_user_dict.pop(uid)
        except:
            pass
    all_influence_user_list = all_influence_user_dict.keys()
    #step2:get uid_list in user_portrait by split all_influence_user
    iter_count = 0
    all_influence_user_count = len(all_influence_user_list)
    in_user_dict = {'domain':{}, 'topic':{}, 'influence':[], 'importance':[]}
    out_user_dict = {}
    in_user_list = []
    out_user_list = []
    while iter_count < all_influence_user_count:
        iter_user_list = all_influence_user_list[iter_count: iter_count + GROUP_ITER_COUNT]
        try:
            in_portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type,\
                            body={'ids':iter_user_list}, _source=False, fields=['uid', 'domain', 'topic_string', 'influence', 'importance'])['docs']
        except:
            in_portrait_result = []
        #step3:get uid_list out user_portrait
        for item in in_portrait_result:
            uid = item['_id']
            if item['found']==True:
                #step4: get user who in user_portrait domain/topic/influence/importance
                domain = item['fields']['domain'][0]
                topic = item['fields']['topic_string'][0]
                topic_list = topic.split('&')
                influence = item['fields']['influence'][0]
                influence_rank = get_index_rank(influence, 'influence')
                importance = item['fields']['importance'][0]
                importance_rank = get_index_rank(importance, 'importance')
                try:
                    in_user_dict['domain'][domain] += 1
                except:
                    in_user_dict['domain'][domain] = 1
                for topic_item in topic_list:
                    try:
                        in_user_dict['topic'][topic_item] += 1
                    except:
                        in_user_dict['topic'][topic_item] = 1
                in_user_dict['influence'].append(influence_rank)
                in_user_dict['importance'].append(importance_rank)
                in_user_list.append(uid)
            else:
                #get user who out user_portrait
                out_user_list.append(uid)
                
            iter_count += GROUP_ITER_COUNT
    #get influence his and importance his
    p, t = np.histogram(in_user_dict['influence'], bins=HIS_BINS_COUNT, normed=False)
    in_user_dict['influence'] = [p.tolist(), [int(item) for item in t.tolist()]]
    p, t = np.histogram(in_user_dict['importance'], bins=HIS_BINS_COUNT, normed=False)
    in_user_dict['importance'] = [p.tolist(), [int(item) for item in t.tolist()]]
    #step5:get user who out user_portrait statusnum/friendsnum/fansnum
    iter_count = 0
    all_out_count = len(out_user_list)
    out_friendsnum_list = []
    out_statusnum_list = []
    out_fansnum_list = []
    while iter_count < all_out_count:
        iter_uid_list = out_user_list[iter_count: iter_count +GROUP_ITER_COUNT]
        try:
            profile_result = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type,\
                                body={'ids':iter_uid_list}, _source=False, \
                                fields=['nick_name', 'statusnum', 'friendsnum', 'fansnum'])['docs']
        except:
            profile_result = []
        for profile_item in profile_result:
            if profile_item['found'] == True:
                out_friendsnum_list.append(profile_item['fields']['friendsnum'][0])
                out_statusnum_list.append(profile_item['fields']['statusnum'][0])
                out_fansnum_list.append(profile_item['fields']['fansnum'][0])
        iter_count += GROUP_ITER_COUNT
    #step6: get out user friendsnum/statusnum/fansnum his
    p, t = np.histogram(out_friendsnum_list, bins=HIS_BINS_COUNT, normed=False)
    out_user_dict['out_friendsnum_his'] = [p.tolist(), [int(item) for item in t.tolist()]]
    p, t = np.histogram(out_statusnum_list, bins=HIS_BINS_COUNT, normed=False)
    out_user_dict['out_statusnum_his'] = [p.tolist(), [int(item) for item in t.tolist()]]
    p, t = np.histogram(out_fansnum_list, bins=HIS_BINS_COUNT, normed=False)
    out_user_dict['out_fansnum_his'] = [p.tolist(), [int(item) for item in t.tolist()]]
    #step7: modify results to do merge
    results['influence_in_user'] = json.dumps(in_user_dict)
    results['influence_out_user'] = json.dumps(out_user_dict)
    return results


#use to get user activity trend
#input: uid_list
#output: results {'activity_trend':[], 'acitivity_time':[dict, description]}
def get_attr_trend(uid_list):
    result = {}
    now_ts = time.time()
    date = ts2datetime(now_ts - DAY)
    #run_type
    if RUN_TYPE == 1:
        timestamp = datetime2ts(date)
    else:
        timestamp = datetime2ts(RUN_TEST_TIME)
    time_result = dict()
    segment_result = dict()
    user_segment_result = dict() # user_segment_result = {uid1:{time_segment1:count1, time_segment2:count2}, uid2:...}
    for i in range(1, 8):
        ts = timestamp - i*DAY
        r_result = redis_activity.hmget('activity_'+str(ts), uid_list)
        iter_count = 0
        for item in r_result:
            if item:
                item = json.loads(item)
                for segment in item:
                    #for all user activity trend
                    try:
                        time_result[int(segment)/16*15*60*16+ts] += item[segment]
                    except:
                        time_result[int(segment)/16*15*60*16+ts] = item[segment]
                    #for user activity time
                    uid = uid_list[iter_count]
                    if uid in user_segment_result:
                        try:
                            user_segment_result[uid][int(segment)/16*15*60*16] += item[segment]
                        except:
                            user_segment_result[uid][int(segment)/16*15*60*16] = item[segment]
                    else:
                        time_key = int(segment)/16*15*60*16
                        user_segment_result[uid] = {time_key: item[segment]}
            iter_count += 1
    trend_list = []
    for i in range(1, 8):
        ts = timestamp - i*DAY
        for j in range(0, 6):
            time_seg = ts + j*15*60*16
            if time_seg in time_result:
                trend_list.append((time_seg, time_result[time_seg]))
            else:
                trend_list.append((time_seg, 0))
    sort_trend_list = sorted(trend_list, key=lambda x:x[0], reverse=False)
    result['activity_trend'] = json.dumps(sort_trend_list)

    #for user activity time
    for uid in uid_list:
        try:
            user_dict = user_segment_result[uid]
        except:
            user_dict = {}
        if user_dict != {}:
            sort_user_dict = sorted(user_dict.items(), key=lambda x:x[1], reverse=True)
            user_main_time = sort_user_dict[0][0]
            try:
                segment_result[user_main_time] += 1
            except:
                segment_result[user_main_time] = 1
    
    sort_segment_result = sorted(segment_result.items(), key=lambda x:x[1], reverse=True)
    top_segment_user_count = sort_segment_result[0][1]
    top_user_ratio = float(top_segment_user_count) / len(uid_list)
    if top_user_ratio >= GROUP_ACTIVITY_TIME_THRESHOLD[-1]:
        activity_time_description = GROUP_ACTIVITY_TIME_DESCRIPTION_DICT['2']
    elif top_user_ratio <= GROUP_ACTIVITY_TIME_THRESHOLD[0]:
        activity_time_description = GROUP_ACTIVITY_TIME_DESCRIPTION_DICT['0']
    else:
        activity_time_description = GROUP_ACTIVITY_TIME_DESCRIPTION_DICT['1']

    result['activity_time'] = json.dumps([segment_result, activity_time_description]) # [(time_segment,user_count), (), (),...]
    
    return result


#use to get week_ave and month_ave rank
def get_evaluate_week_month_ave_rank(value, item_key, evaluate_index):
    query_body = {
    'query':{
        'range': {item_key:{'gte': value}}
        }
    }
    if evaluate_index == 'bci':
        index_rank = ES_COPY_USER_PORTRAIT.count(index=COPY_USER_PORTRAIT_INFLUENCE, doc_type=COPY_USER_PORTRAIT_INFLUENCE, body=query_body)
    elif evaluate_index == 'activeness':
        index_rank = ES_COPY_USER_PORTRAIT.count(index=COPY_USER_PORTRAIT_ACTIVENESS, doc_type=COPY_USER_PORTRAIT_ACTIVENESS, body=query_body)
    if index_rank['_shards']['successful'] != 0:
        ave_rank = index_rank['count']
    else:
        ave_rank = 0
        print 'es index rank error'
    return ave_rank

# write in version: 16-03-27
def get_evaluate_ts_dict(history_dict, evaluate_index):
    ts_evaluate_dict = {} # {ts1: {uid1:index1, uid2:index2,..},...}
    evaluate_week_ave = {}
    evaluate_month_ave = {}
    for user_history_item in history_dict:
        uid = user_history_item['_id']
        if user_history_item['found'] == True:
            source = user_history_item['_source']
            for item in source:
                item_list = item.split('_')
                if len(item_list) == 2 and item_list[0]==evaluate_index:
                    evaluate_ts = int(item_list[1])
                    if evaluate_ts in ts_evaluate_dict:
                        ts_evaluate_dict[evaluate_ts][uid] = source[item]
                    else:
                        ts_evaluate_dict[evaluate_ts] = {uid: source[item]}
                elif item == evaluate_index + '_week_ave':
                    evaluate_week_ave_rank = get_evaluate_week_month_ave_rank(source[item], item, evaluate_index)
                    evaluate_week_ave[uid] = [source[item], evaluate_week_ave_rank]
                elif item == evaluate_index + '_month_ave':
                    evaluate_month_ave_rank = get_evaluate_week_month_ave_rank(source[item], item, evaluate_index)
                    evaluate_month_ave[uid] = [source[item], evaluate_month_ave_rank]
    #deal the machine is power off
    now_date_ts = datetime2ts(ts2datetime(time.time()))
    min_date_ts = min(ts_evaluate_dict.keys())
    for i in range(1, 31, 1):
        iter_date_ts = now_date_ts - i * DAY
        if iter_date_ts < min_date_ts:
            break
        if iter_date_ts not in ts_evaluate_dict:
            ts_evaluate_dict[iter_date_ts] = {}
    return ts_evaluate_dict, evaluate_week_ave, evaluate_month_ave

def get_all_copy_user_portrait_count():
    all_user_count = 0
    query_body = {
    'query':{
        'match_all':{}
        }
    }
    result = ES_COPY_USER_PORTRAIT.count(index=COPY_USER_PORTRAIT_INFLUENCE, doc_type=COPY_USER_PORTRAIT_INFLUENCE_TYPE, body=query_body)
    if result['_shards']['successful'] != 0:
        all_user_count = result['count']
    else:
        all_user_count = 0
        print 'es index rank error'
    return all_user_count

def get_evaluate_ratio_dis(evaluate_ave_dict, all_portrait_count):
    evaluate_ave_index_dis = {}
    evaluate_ave_top_user = []
    all_user_count = len(evaluate_ave_dict )
    for uid in evaluate_ave_dict:
        value_rank_list = evaluate_ave_dict[uid]
        value = value_rank_list[0]
        rank = value_rank_list[1]
        evaluate_ratio = get_index_rank_ratio(rank, all_portrait_count)
        try:
            evaluate_ave_index_dis[evaluate_ratio] += 1       
        except:
            evaluate_ave_index_dis[evaluate_ratio] = 1
    sort_evaluate_ave = sorted(evaluate_ave_dict.items(), key=lambda x:x[1][0], reverse=True)
    evaluate_ave_top_user =[item[0] for item in sort_evaluate_ave]

    return evaluate_ave_index_dis, evaluate_ave_top_user


#use to get user evaluate index trend
#input: uid_list
#output: evaluate_index_trend
def get_attr_evaluate_trend(uid_list):
    results = {}
    activeness_dict = {} # {ts1:{uid:index, uid:index}, ts2:{}, ts3:{},...}
    influence_dict = {} # {ts1:{uid:index, uid:index}, ts2:{}, ...}
    #old for abandon
    try:
        es_user_result = es_copy_portrait.mget(index=copy_portrait_index_name, doc_type=copy_portrait_index_type, \
                body={'ids':uid_list})['docs']
    except:
        es_user_result = []
    #new for new activeness history
    try:
        activeness_history = ES_COPY_USER_PORTRAIT.mget(index=COPY_USER_PORTRAIT_ACTIVENESS,\
                doc_type=COPY_USER_PORTRAIT_ACTIVENESS_TYPE, body={'ids':uid_list})['docs']
    except:
        activeness_history = []
    #new for new influence trend
    try:
        influence_history = ES_COPY_USER_PORTRAIT.mget(index=COPY_USER_PORTRAIT_INFLUENCE,\
                doc_type=COPY_USER_PORTRAIT_INFLUENCE_TYPE, body={'ids':uid_list})['docs']
    except:
        influence_history = []
    #new for get activeness_dict
    activeness_dict, activeness_week_ave_dict, activeness_month_ave_dict = get_evaluate_ts_dict(activeness_history, 'activeness')
    #new for get influence dict
    influence_dict, influence_week_ave_dict, influence_month_ave_dict = get_evaluate_ts_dict(influence_history, 'bci')
    #get all user count
    all_portrait_count = get_all_copy_user_portrait_count()   
    #get evaluate rank ratio dis
    influence_week_ave_dis, influence_week_ave_top_user = get_evaluate_ratio_dis(influence_week_ave_dict, all_portrait_count)
    influence_month_ave_dis, influence_month_ave_top_user = get_evaluate_ratio_dis(influence_month_ave_dict, all_portrait_count)
    activeness_week_ave_dis, activeness_week_ave_top_user = get_evaluate_ratio_dis(activeness_week_ave_dict, all_portrait_count)
    activeness_month_ave_dis, activeness_month_ave_top_user = get_evaluate_ratio_dis(activeness_month_ave_dict, all_portrait_count)
    #get activeness trend--ave_value/min_value/max_value
    activeness_time_list = []
    ave_list = []
    max_list = []
    min_list = []
    #get uname by uid
    uid2uname = {}
    try:
        user_portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type, \
                body={'ids':uid_list}, _source=False, fields=['uname'])['docs']
    except:
        user_portrait_result = []
    for item in user_portrait_result:
        uid = item['_id']
        if item['found'] == True:
            uname = item['fields']['uname'][0]
            uid2uname[uid] = uname
    #get influence week ave top user/month ave top user
    influence_week_ave_top_uname = []
    for top_uid in influence_week_ave_top_user:
        try:
            top_uname = uid2uname[top_uid]
        except:
            top_uname = top_uid
        influence_week_ave_top_uname.append(top_uname)
    influence_month_ave_top_uname = []
    for top_uid in influence_month_ave_top_user:
        try:
            top_uname = uid2uname[top_uid]
        except:
            top_uname = top_uid
    #get activeness week ave top user/month ave top user
    activeness_week_ave_top_uname = []
    for top_uid in influence_month_ave_top_user:
        try:
            top_uname = uid2uname[top_uid]
        except:
            top_uname = top_uid
        activeness_week_ave_top_uname.append(top_uname)
    activeness_month_ave_top_uname = []
    for top_uid in activeness_month_ave_top_user:
        try:
            top_uname = uid2uname[top_uid]
        except:
            top_uname = top_uid
        activeness_month_ave_top_uname.append(top_uname)
    #get ts activeness trend and top
    sort_activeness_dict = sorted(activeness_dict.items(), key=lambda x:x[0])
    main_max_activeness_dict = {}
    main_min_activeness_dict = {}
    for ts_item in sort_activeness_dict:
        timestamp = ts_item[0]
        ts_index_dict = ts_item[1]
        activeness_time_list.append(ts2datetime(timestamp))
        try:
            ave_value = float(sum(ts_index_dict.values())) / len(ts_index_dict)
        except:
            ave_value = 0
        sort_ts_index = sorted(ts_index_dict.items(), key=lambda x:x[1], reverse=True)
        ave_list.append(ave_value)
        #get max/min uid-uname
        try:
            max_uname = uid2uname[sort_ts_index[0][0]]
        except:
            max_uname = ''
        try:
            min_uname = uid2uname[sort_ts_index[-1][0]]
        except:
            min_uname = ''
        if max_uname != '':
            max_list.append([sort_ts_index[0][0], sort_ts_index[0][1], max_uname])
        else:
            max_list.append(['', 0 , ''])
        if min_uname != '':
            min_list.append([sort_ts_index[-1][0], sort_ts_index[-1][1], min_uname])
        else:
            min_list.append(['', 0, ''])
        #get main max uid-uname
        if max_uname != '':
            max_uid_uname = sort_ts_index[0][0] + '&' + max_uname
            try:
                main_max_activeness_dict[max_uid_uname] += 1
            except:
                main_max_activeness_dict[max_uid_uname] = 1
        #get main min uid-uname
        if min_uname != '':
            min_uid_uname = sort_ts_index[-1][0] + '&' + min_uname
            try:
                main_min_activeness_dict[min_uid_uname] += 1
            except:
                main_min_activeness_dict[min_uid_uname] = 1
    
    sort_main_max_activeness = sorted(main_max_activeness_dict.items(), key=lambda x:x[1], reverse=True)
    sort_main_min_activeness = sorted(main_min_activeness_dict.items(), key=lambda x:x[1], reverse=True)
    results['activeness'] =json.dumps({'time_list':activeness_time_list, 'ave_list':ave_list, 'max_list':max_list,\
            'min_list':min_list, 'main_max':sort_main_max_activeness[:5], 'main_min':sort_main_min_activeness[:5], 'week_ave_dis':activeness_week_ave_dis, 'month_ave_dis': activeness_month_ave_dis, 'week_ave_top_user': activeness_week_ave_top_uname, 'month_ave_top_user': activeness_month_ave_top_uname})        #get influence trend--ave_value/min_value/max_value
    influence_time_list = []
    ave_list = []
    max_list = []
    min_list = []
    sort_influence_dict = sorted(influence_dict.items(), key=lambda x:x[0])
    main_max_influence_dict = {}
    main_min_influence_dict = {}
    for ts_item in sort_influence_dict:
        timestamp = ts_item[0]
        ts_index_dict = ts_item[1]
        influence_time_list.append(ts2datetime(timestamp))
        try:
            ave_value = float(sum(ts_index_dict.values())) / len(ts_index_dict)
        except:
            ave_value = 0
        ave_list.append(ave_value)
        sort_ts_index = sorted(ts_index_dict.items(), key=lambda x:x[1], reverse=True)
        #get max/min uid-uname
        try:
            max_uname = uid2uname[sort_ts_index[0][0]]
        except:
            max_uname = ''
        try:
            min_uname = uid2uname[sort_ts_index[-1][0]]
        except:
            min_uname = ''
        if max_uname != '':
            max_list.append([sort_ts_index[0][0], sort_ts_index[0][1], max_uname])
        else:
            max_list.append(['', 0, ''])
        if min_uname != '':
            min_list.append([sort_ts_index[-1][0], sort_ts_index[-1][1], min_uname])
        else:
            min_list.append(['', 0, ''])
        #get main max uid-uname
        if max_uname != '':
            max_uid_uname = sort_ts_index[0][0] + '&' + max_uname
            try:
                main_max_influence_dict[max_uid_uname] += 1
            except:
                main_max_influence_dict[max_uid_uname] = 1
        #get main min uid-uname
        if min_uname != '':
            min_uid_uname = sort_ts_index[-1][0] + '&' + min_uname
            try:
                main_min_influence_dict[min_uid_uname] += 1
            except:
                main_min_influence_dict[min_uid_uname] = 1
    
    sort_main_max_influence = sorted(main_max_influence_dict.items(), key=lambda x:x[1], reverse=True)
    sort_main_min_influence = sorted(main_min_influence_dict.items(), key=lambda x:x[1], reverse=True)
    results['influence'] = json.dumps({'time_list':influence_time_list, 'ave_list':ave_list, 'max_list':max_list,\
            'min_list':min_list, 'main_max':sort_main_max_influence[:5], 'main_min':sort_main_min_influence[:5], 'week_ave_dis': influence_week_ave_dis, 'month_ave_dis': influence_month_ave_dis, 'week_ave_top_user': influence_week_ave_top_uname, 'month_ave_top_user': influence_month_ave_top_uname})    
    
    return results

#use to get sentiment trend
#input: uid_list
#output: sentiment trend and main sentiment ratio
def get_attr_sentiment_trend(uid_list):
    results = {}
    ts_sentiment_dict = {} #for 0, 1, 2 senitment
    ts_all_sentiment_dict = {} # for 0,1,2,3,4,5,6 sentiment
    ts_all_sentiment_dict = {'0':0, '1':0, '2':0, '3':0, '4':0, '5':0, '6':0}
    week_sentiment_trend = {}
    #step1:get now date ts
    now_ts = int(time.time())
    #run_type
    if RUN_TYPE == 1:
        now_date_ts = datetime2ts(ts2datetime(now_ts))
    else:
        now_date_ts = datetime2ts(RUN_TEST_TIME)
    #step2:iter to search flow text es
    for i in range(7, 0, -1):
        iter_date_ts = now_date_ts - i * DAY
        iter_date = ts2datetime(iter_date_ts)
        flow_text_index_name = flow_text_index_name_pre + str(iter_date)
        
        try:
            flow_text_result = es_flow_text.search(index=flow_text_index_name, doc_type=flow_text_index_type ,\
                    body={'query':{'terms':{'uid': uid_list}}, 'size': MAX_VALUE}, _source=False, fields=['sentiment'])['hits']['hits']
        except:
            flow_text_result = []
        ts_sentiment_dict[iter_date_ts] = {'0':0, '1':0, '2':0, '3':0}
        for flow_text_item in flow_text_result:
            sentiment = str(flow_text_item['fields']['sentiment'][0])
            #count for all sentiment
            ts_all_sentiment_dict[sentiment] += 1
            #count for three sentiment 0,1,2
            if sentiment != '0' and sentiment != '1':
                sentiment = '2'
            ts_sentiment_dict[iter_date_ts][sentiment] += 1
    #step3: sort by ts and make trend list
    sort_ts_sentiment_dict = sorted(ts_sentiment_dict.items(), key=lambda x:x[0])
    time_list = [ts2datetime(item[0]) for item in sort_ts_sentiment_dict]
    sentiment_trend_dict = {} # {'1':[count1, count2,...], '2':[], '0':[]}  count ranked by time_list
    for sentiment in GROUP_SENTIMENT_LIST:
        date_sentiment_trend = [item[1][sentiment] for item in sort_ts_sentiment_dict]
        try:
            week_sentiment_trend[sentiment].extend(date_sentiment_trend)
        except:
            week_sentiment_trend[sentiment] = date_sentiment_trend
    try:
        week_sentiment_trend['time_list'].extend(time_list)
    except:
        week_sentiment_trend['time_list'] = time_list

    #step3:main negative sentiment
    main_negative_dict = {}
    for sentiment in GROUP_NEGATIVE_SENTIMENT:
        sentiment_count = ts_all_sentiment_dict[sentiment]
        main_negative_dict[sentiment] = sentiment_count
    sort_main_negative_dict = sorted(main_negative_dict.items(), key=lambda x:x[1], reverse=True)
    
    #step4: results
    results['sentiment_trend'] = json.dumps(week_sentiment_trend)
    results['sentiment_pie'] = json.dumps(ts_all_sentiment_dict)
    #tag vector---main negative
    tag_vector_result = {}
    tag_vector_result['main_negative_sentiment'] = [u'主要消极情绪', sort_main_negative_dict[0][0]]
    return results, tag_vector_result


#use to get user using sentiment keywords
#input: uid_list
#output: results {word1:count, word2:count,...}
def get_attr_sentiment_word(uid_list):
    results = {}
    now_ts = int(time.time())
    now_date_ts = datetime2ts(ts2datetime(now_ts))
    # get information from redis by iter date and split user to iter
    iter_count = 0
    user_count = len(uid_list)
    iter_result_list = []
    week_sentiment_word_result = []
    while iter_count < user_count:
        iter_uid_list = uid_list[iter_count: iter_count + GROUP_ITER_COUNT]
        week_result_list = []
        for i in range(7, 0, -1):
            iter_ts = now_date_ts - i * DAY
            try:
                sentiment_word_result = redis_cluster.hmget('sensitive_'+str(iter_ts), uid_list)
            except:
                sentiment_word_result = []
            #filter null item in sentiment word result
            new_sentiment_word_result = [item for item in sentiment_word_result if item != None]
            if new_sentiment_word_result != []:
                sentiment_word_result = [json.loads(s) for s in sentiment_word_result if isinstance(s, str)]
                date_sentiment_word_result = union_dict_list(sentiment_word_result)
                week_result_list.append(date_sentiment_word_result)
        if week_result_list != []:
            week_sentiment_word_result = union_dict_list(week_result_list)
        if iter_result_list != []:
            iter_result_list.append(week_sentiment_word_result)
        iter_count += GROUP_ITER_COUNT
    if iter_result_list != []:
        results = union_dict_list(iter_result_list)
    # statistic
    sort_results = sorted(results.items(), key=lambda x:x[1], reverse=True)[:GROUP_SENTIMENT_WORD_COUNT]
    # modify result to merge
    results  = {'sentiment_word': json.dumps(sort_results)}
    return results



# get importance max & activeness max & influence max to normalize
def get_evaluate_max():
    max_result = {}
    index_name = 'user_portrait'
    index_type = 'user'
    evaluate_index = ['activeness', 'importance', 'influence']
    for evaluate in evaluate_index:
        query_body = {
            'query': {
                'match_all':{}
                },
            'size': 1,
            'sort': [{evaluate:{'order': 'desc'}}]
            }
        try:
            result = es.search(index=index_name, doc_type=index_type, body=query_body)['hits']['hits']
        except Exception, e:
            raise e
        max_evaluate = result[0]['_source'][evaluate]
        max_result[evaluate] = max_evaluate

    return max_result

#use to normal evaluate trend max
#input: index_key
#output: max_value
def get_evaluate_max_trend(index_key):
    query_body = {
            'query':{
                'match_all':{}
                },
            'size': 1,
            'sort': [{index_key: {'order': 'desc'}}]
        }
    try:
        index_max_value = es_user_portrait.search(index=copy_portrait_index_name, doc_type=copy_portrait_index_type, body=query_body)['hits']['hits']
    except Exception, e:
        raise e
    index_max = index_max_value[0]['_source'][index_key]
    return index_max



def get_attr_bci(uid_list):
    results = []
    now_ts = time.time()
    now_date = ts2datetime(now_ts - 24*3600)
    ts = datetime2ts(now_date)
    #test
    ts = datetime2ts('2013-09-07')
    user_results = {} # {'uid':{'origin_max..':[], ''}}
    total_weibo_number = 0
    
    fans_number = 0
    origin_weibo_number = 0
    retweeted_weibo_number = 0
    origin_weibo_retweeted_total_number = 0
    origin_weibo_comment_total_number = 0
    retweeted_weibo_retweeted_total_number = 0
    retweeted_weibo_comment_total_number = 0

    origin_weibo_retweeted_top = 0
    origin_weibo_comment_top = 0
    retweeted_weibo_retweeted_top = 0
    retweeted_weibo_comment_top = 0
    influence_dict = {}

    for i in range(0, 7):
        timestamp = ts - i*DAY
        date = ts2datetime(timestamp)
        hash_key = ''.join(date.split('-'))
        es_user_results = es_cluster.mget(index=hash_key, doc_type='bci', body={'ids':uid_list})['docs']
        for user_dict in es_user_results:
            try:
                user_item = user_dict['_source']
            except:
                next
            uid = user_item['user']
            total_weibo_number += user_item['origin_weibo_number']
            total_weibo_number += user_item['retweeted_weibo_number']
            
            # yuankun revise
            origin_weibo_number += user_item['origin_weibo_number']
            retweeted_weibo_number += user_item['retweeted_weibo_number']
            origin_weibo_retweeted_top += user_item['origin_weibo_retweeted_top_number']
            origin_weibo_comment_top += user_item['origin_weibo_comment_top_number']
            retweeted_weibo_retweeted_top += user_item['retweeted_weibo_retweeted_top_number']
            retweeted_weibo_comment_top += user_item['retweeted_weibo_comment_top_number']
            #print 'user_item:', user_item
            if uid in user_results:
                try:
                    user_results[uid]['origin_weibo_retweeted_top'].append([user_item['origin_weibo_retweeted_top_number'], user_item['origin_weibo_top_retweeted_id']])
                    user_results[uid]['origin_weibo_comment_top'].append([user_item['origin_weibo_comment_top_number'], user_item['origin_weibo_top_comment_id']])
                    user_results[uid]['retweeted_weibo_retweeted_top'].append([user_item['retweeted_weibo_retweeted_top_number'], user_item['retweeted_weibo_top_retweeted_id']])
                    user_results[uid]['retweeted_weibo_comment_top'].append([user_item['retweeted_weibo_comment_top_number'], user_item['retweeted_weibo_top_comment_id']])
                except:
                    user_results[uid]['origin_weibo_retweeted_top'] = [[user_item['origin_weibo_retweeted_top_number'], user_item['origin_weibo_top_retweeted_id']]]
                    user_results[uid]['origin_weibo_comment_top'] = [[user_item['origin_weibo_comment_top_number'], user_item['origin_weibo_top_comment_id']]]
                    user_results[uid]['retweeted_weibo_retweeted_top'] = [[user_item['retweeted_weibo_retweeted_top_number'], user_item['retweeted_weibo_top_retweeted_id']]]
                    user_results[uid]['retweeted_weibo_comment_top'] = [[user_item['retweeted_weibo_comment_top_number'], user_item['retweeted_weibo_top_comment_id']]]
            else:
                #print 'user_item:', [[user_item['origin_weibo_retweeted_top_number'], user_item['origin_weibo_top_retweeted_id']]]
                user_results[uid] = {'origin_weibo_retweeted_top':[[user_item['origin_weibo_retweeted_top_number'], user_item['origin_weibo_top_retweeted_id']]]}
                user_results[uid] = {'origin_weibo_comment_top': [[user_item['origin_weibo_comment_top_number'], user_item['origin_weibo_top_comment_id']]]}
                user_results[uid] = {'retweeted_weibo_retweeted_top': [[user_item['retweeted_weibo_retweeted_top_number'], user_item['retweeted_weibo_top_retweeted_id']]]}
                user_results[uid] = {'retweeted_weibo_comment_top': [[user_item['retweeted_weibo_comment_top_number'], user_item['retweeted_weibo_top_comment_id']]]}
            
            # yuankun need
            #print 'fan_num:', user_item['user_fansnum'], type(user_item['user_fansnum']), type(fans_number)
            fans_number += int(user_item['user_fansnum'])
            origin_weibo_retweeted_total_number += user_item['origin_weibo_retweeted_total_number']
            origin_weibo_comment_total_number += user_item['origin_weibo_comment_total_number']
            retweeted_weibo_retweeted_total_number += user_item['retweeted_weibo_retweeted_total_number']
            retweeted_weibo_comment_total_number += user_item['retweeted_weibo_comment_total_number']

    user_portrait_result = es.mget(index='user_portrait', doc_type='user', body={'ids':uid_list})['docs']
    #print 'user_portrait_result:', user_portrait_result[0]

    # get activeness max & importance max & influence max to normalize
    evaluate_max_result = get_evaluate_max()

    for user_portrait in user_portrait_result:
        #print 'user_portrait:', user_portrait
        try:
            user_portrait_dict = user_portrait['_source']
            #print 'user_portrait_dict:', user_portrait_dict
            uname = user_portrait_dict['uname']
            importance = user_portrait_dict['importance']
            normal_importance = math.log((importance / evaluate_max_result['importance']) * 9 + 1, 10) * 100
            activeness = user_portrait_dict['activeness']
            normal_activeness = math.log(activeness / evaluate_max_result['activeness'] * 9 + 1, 10) * 100
            influence = user_portrait_dict['influence']
            normal_influence = math.log(influence / evaluate_max_result['influence'] * 9 + 1, 10) * 100
        except:
            uname = ''
            normal_importance = ''
            normal_activeness = ''
            normal_influence = ''
        #print 'user_portrait_dict:', user_portrait_dict
        uid = user_portrait_dict['uid']
        user_item_dict = user_results[uid]
        origin_weibo_retweeted_top_item = sorted(user_item_dict['origin_weibo_retweeted_top'], key=lambda x:x[0], reverse=True)[0]
        origin_weibo_comment_top_item = sorted(user_item_dict['origin_weibo_comment_top'], key=lambda x:x[0], reverse=True)[0]
        retweeted_weibo_retweeted_top_item = sorted(user_item_dict['retweeted_weibo_retweeted_top'], key=lambda x:x[0], reverse=True)[0]
        retweeted_weibo_comment_top_item = sorted(user_item_dict['retweeted_weibo_comment_top'], key=lambda x:x[0], reverse=True)[0]
        
        results.append([uid, uname, normal_activeness, normal_importance, normal_influence, origin_weibo_retweeted_top_item ,\
                        origin_weibo_comment_top_item, retweeted_weibo_retweeted_top_item, \
                        retweeted_weibo_comment_top_item])

    #yuankun need
    influence_dict['origin_weibo_retweeted_average_number'] = origin_weibo_retweeted_total_number/origin_weibo_number/7
    influence_dict['origin_weibo_comment_average_number'] = origin_weibo_comment_total_number/origin_weibo_number/7
    influence_dict['retweeted_weibo_retweeted_average_number'] = retweeted_weibo_retweeted_total_number/retweeted_weibo_number/7
    influence_dict['retweeted_weibo_comment_average_number'] = retweeted_weibo_comment_total_number/retweeted_weibo_number/7
    influence_dict['origin_weibo_retweeted_top_number'] = origin_weibo_retweeted_top/len(uid_list)/7
    influence_dict['origin_weibo_comment_top_number'] = origin_weibo_comment_top/len(uid_list)/7
    influence_dict['retweeted_weibo_retweeted_top_number'] = retweeted_weibo_retweeted_top/len(uid_list)/7
    influence_dict['retweeted_weibo_comment_top_number'] = retweeted_weibo_comment_top/len(uid_list)/7
    influence_dict['fans_number'] = fans_number
    influence_dict['total_weibo_number'] = total_weibo_number
    #print 'results:', results
    return {'user_influence_list': json.dumps(results), 'total_weibo_number': total_weibo_number}, influence_dict


# yuankun revise
def get_attr_influence(uid_list, bci_dict):
    result = {}
    weight = [0.3, 0.4, 0.2, 0.1]
    influence = weight[0]*(0.3*math.log(1+bci_dict['origin_weibo_retweeted_top_number'])+0.3*math.log(1+bci_dict['origin_weibo_comment_top_number'])+\
                0.2*math.log(1+bci_dict['retweeted_weibo_retweeted_top_number'])+0.2*math.log(1+bci_dict['retweeted_weibo_comment_top_number'])) + \
                weight[1]*(0.3*math.log(1+bci_dict['origin_weibo_retweeted_average_number'])+0.3*math.log(1+bci_dict['origin_weibo_comment_average_number']) + \
                0.2*math.log(1+bci_dict['retweeted_weibo_retweeted_average_number'])+0.2*math.log(1+bci_dict['retweeted_weibo_comment_average_number'])) + \
                weight[2]*math.log(1+bci_dict['fans_number']) + weight[3]*math.log(1+bci_dict['total_weibo_number'])
    influence = 300 * influence

    result['influence'] = influence
    return result # result = {'influence': count}


def get_attr_activeness(activity_trend, total_number, activity_geo):
    result = dict()
    sort_activity_trend = sorted(activity_trend, key=lambda x:x[0], reverse=False)
    activity_list = [item[1] for item in sort_activity_trend]
    signal = np.array(activity_list)
    fftResult = np.abs(np.fft.fft(signal)) ** 2
    n = signal.size
    freq = np.fft.fftfreq(n, d=1)
    i = 0
    max_val = 0
    max_freq = 0
    for val in fftResult:
        if val>max_val and freq[i]>0:
            max_val = val
            max_freq = freq[i]
        i = i + 1
    result['activeness'] = activeness_weight_dict['activity_time'] * math.log(max_freq + 1) +\
             activeness_weight_dict['activity_geo'] * math.log(len(activity_geo) + 1) +\
             activeness_weight_dict['statusnum'] * math.log(total_number + 1)
    return result


def get_attr_importance(domain_dict, topic_dict, count, be_retweeted_count, be_retweeted_weibo_count):
    result = dict()
    sort_domain = sorted(domain_dict.items(), key=lambda x:x[1], reverse=True)
    sort_topic = sorted(topic_dict.items(), key=lambda x:x[1], reverse=True)
    domain_list = sort_domain[:5]
    topic_list = sort_topic[:5]
    domain_result = 0
    for domain in domain_list:
        try:
            domain_result = domain_weight_dict[domain] * domain_dict[domain]
        except:
            pass
    topic_result = 0
    for topic in topic_list:
        try:
            topic_result = topic_weight_dict[topic] * topic_dict[topic]
        except:
            pass
    result['importance'] = importance_weight_dict['count'] * math.log(count + 1) + \
                           importance_weight_dict['topic'] * math.log(topic_result + 1) + \
                           importance_weight_dict['domain'] * math.log(domain_result + 1) +\
                           importance_weight_dict['be_retweeted_out'] * math.log(be_retweeted_count + 1) +\
                           importance_weight_dict['be_retweeted_count_out'] * math.log(be_retweeted_weibo_count + 1)

    return result

def get_attr_tightness(density, retweet_weibo_count, retweet_user_count):
    result = dict()
    result['tightness'] = tightness_weight_dict['density'] * math.log(density + 1) +\
                          tightness_weight_dict['retweet_weibo_count'] * math.log(retweet_weibo_count + 1) +\
                          tightness_weight_dict['retweet_user_count'] * math.log(retweet_user_count + 1)
    return result


def ip2geo(ip_dict):
    city_set = set()
    geo_dict = dict()
    for ip in ip_dict:
        try:
            city = IP.find(str(ip))
            if city:
                city.encode('utf-8')
            else:
                city = ''
        except Exception, e:
            city = ''
        if city:
            len_city = len(city.split('\t'))
            if len_city==4:
                city = '\t'.join(city.split('\t')[:3])
            city_list = city.split('\t')
            city = city_list[len(city_list)-1]
            try:
                geo_dict[city] += ip_dict[ip]
            except:
                geo_dict[city] = ip_dict[ip]
    return geo_dict

#use to get group tag to uid_list
#write in version: 16-03-18
def add_group_tag(submit_user, task_name, uid_list):
    bulk_action = []
    #step1: get uid_list user_portrait old group field value
    try:
        user_portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type,\
                body={'ids': uid_list})['docs']
    except:
        user_portrait_result = []
    #step2: update group field value
    for user_portrait_item in user_portrait_result:
        uid = user_portrait_item['_id']
        try:
            source = user_portrait_item['_source']
        except:
            source = {}
        try:
            group_tag = source['group']
        except:
            group_tag = ''
        if group_tag != '':
            new_group_tag = group_tag + '&' + submit_user + '-' + task_name
        else:
            new_group_tag = submit_user + '-' + task_name
        update_dict = {'group': new_group_tag}
        action = {'update': {'_id': uid}}
        bulk_action.extend([action, {'doc': update_dict}])
    #step3: save bulk action to update
    if bulk_action:
        es_user_portrait.bulk(bulk_action, index=portrait_index_name, doc_type=portrait_index_type)


#user to get topic model results
#version: 16-03-26
#input: uid_list
def get_attr_topic_model(uid_list):
    weibo_list = []
    results = []
    #run_type
    if RUN_TYPE == 1:
        now_date = ts2datetime(int(time.time()))
    else:
        now_date = RUN_TEST_TIME
    now_date_ts = datetime2ts(now_date)
    #step1:get user weibo list
    for i in range(7, 0, -1):
        iter_date_ts = now_date_ts - i * DAY
        iter_date = ts2datetime(iter_date_ts)
        flow_text_index_name = flow_text_index_name_pre + iter_date
        try:
            weibo_exist = es_flow_text.search(index=flow_text_index_name, doc_type=flow_text_index_type,\
                    body={'query':{'filtered':{'filter':{'terms':{'uid': uid_list}}}}, 'size': MAX_VALUE}, _source=False, fields=['text'])['hits']['hits']
        except:
            weibo_exist = []
        for weibo_item in weibo_exist:
            weibo_text = weibo_item['fields']['text'][0]
            if isinstance(weibo_text, unicode):
                weibo_text = weibo_text.encode('utf-8')
            weibo_list.append(weibo_text)
    #step2:use lda_main(texts, nt)
    #result_list = topic_lda_main(weibo_list, TOPIC_MODEL_COUNT)
    result_list = topic_lda_main(weibo_list)
    #step3: get keywords
    topic_result = []
    result_list = result_list[:10]
    for result_item in result_list:
        result_item_list = result_item[1].split('+')
        word_list = [result_string_item.split('*')[1] for result_string_item in result_item_list]
        topic_result.append(word_list)
    return topic_result

#use to compute group task for multi-process
#version: 16-02-27
def compute_group_task_v2():
    results = dict()
    while True:
        task = r.rpop(group_analysis_queue_name)
        #test
        #r.lpush(group_analysis_queue_name, task)
        if not task:
            break
        else:
            results = dict()
            task = json.loads(task)
            task_name = task['task_name']
            uid_list = task['uid_list']
            submit_date = task['submit_date']  #submit_date = timestamp
            results['task_type'] = task['task_type']
            results['count'] = len(uid_list)
            results['task_id'] = task['submit_user'] + task_name
            #get uid2uname dict for other module using
            uid2uname = {}
            try:
                portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type,\
                                              body={'ids':uid_list},  _source=False, fields=['uname'])['docs']
            except:
                portrait_result = []
            for item in portrait_result:
                uid = item['_id']
                if item['found'] == True:
                    uname = item['fields']['uname'][0]
                uid2uname[uid] = uname

            #step1: get attr from es_user_portrait--basic/activity_geo/online_pattern/evaluate_index_his/preference/psycho_ratio
            uid_list = uid2uname.keys() #identify the uid is in user_portrait
            submit_user = task['submit_user']

            print 'get_attr_portrait'
            attr_in_portrait, tag_vector_result = get_attr_portrait(uid_list, submit_user)
            results['task_name'] = task_name
            results['uid_list'] = uid_list
            results['submit_date'] = submit_date
            results['state'] = task['state']
            results['submit_user'] = task['submit_user']
            results = dict(results, **attr_in_portrait)

            #step2: get attr from social es----es_retweet&es_comment
            print 'get_attr_social'
            attr_in_social = get_attr_social(uid_list, uid2uname)
            results = dict(results, **attr_in_social)

            #step3: get attr activity trend and activity_time----redis for activity time
            print 'get_attr_trend'
            attr_weibo_trend = get_attr_trend(uid_list) # {'activity_trend':[], 'activity_time':{}}
            results = dict(results, **attr_weibo_trend)
            #step4: get evaluate index trend----copy_user_portrait
            print 'get_attr_evaluate_trend'
            evaluate_index_trend_dict = get_attr_evaluate_trend(uid_list) # {'importance_trend':[], 'influence_trend❯
            results = dict(results, **evaluate_index_trend_dict)
            #step5: get sentiment trend----flow_text_es
            print 'get_attr_sentiment_trend'
            sentiment_trend, sentiment_tag_vector = get_attr_sentiment_trend(uid_list)
            results = dict(results, **sentiment_trend)
            tag_vector_result = dict(tag_vector_result, **sentiment_tag_vector)
            #step6: get influence user
            print 'get_attr_influence_user'
            influence_user_result = get_influence_user(uid_list)
            results = dict(results, **influence_user_result)
            #step7: get user sentiment words
            print 'get_attr_sentiment_word'
            user_sentiment_words = get_attr_sentiment_word(uid_list)
            results = dict(results, **user_sentiment_words)
            results['tag_vector'] = json.dumps(tag_vector_result)
            #step8: get user topic model
            print 'get_attr_topic_model'
            user_topic_results = get_attr_topic_model(uid_list)
            results['topic_model'] = json.dumps(user_topic_results)
            #step8: update compute status to completed
            results['status'] = 1
            #step9: save results
            save_group_results(results)
            #step10: add group tag
            add_group_tag(results['submit_user'], task_name, uid_list)
            #test
            #break 


#test compute group task
#input: NULL
#output: 
def compute_group_task():
    results = dict()
    task = json.loads(TASK)
    task_name = task['task_name']
    uid_list = task['uid_list']
    submit_date = task['submit_date']  #submit_date = timestamp
    results['task_type'] = task['task_type']
    results['count'] = len(uid_list)
    results['task_id'] = task['task_id']
    #get uid2uname dict for other module using
    uid2uname = {}
    try:
        portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type,\
                            body={'ids':uid_list},  _source=False, fields=['uname'])['docs']
    except:
        portrait_result = []
    for item in portrait_result:
        uid = item['_id']
        if item['found'] == True:
            uname = item['fields']['uname'][0]
            uid2uname[uid] = uname
    #step1: get attr from es_user_portrait--basic/activity_geo/online_pattern/evaluate_index_his/preference/psycho_ratio
    uid_list = uid2uname.keys()
    submit_user = task['submit_user']
    attr_in_portrait, tag_vector_result = get_attr_portrait(uid_list, submit_user)
    results['task_name'] = task_name
    results['uid_list'] = uid_list
    results['submit_date'] = submit_date
    results['state'] = task['state']
    results['submit_user'] = task['submit_user']
    results = dict(results, **attr_in_portrait)
    #step2: get attr from social es----es_retweet&es_comment
    attr_in_social = get_attr_social(uid_list, uid2uname)
    results = dict(results, **attr_in_social)
    #step3: get attr activity trend and activity_time----redis for activity time
    attr_weibo_trend = get_attr_trend(uid_list) # {'activity_trend':[], 'activity_time':{}}
    results = dict(results, **attr_weibo_trend)
    #step4: get evaluate index trend----copy_user_portrait
    evaluate_index_trend_dict = get_attr_evaluate_trend(uid_list) # {'importance_trend':[], 'influence_trend':[], 'importance_trend':[]}
    results = dict(results, **evaluate_index_trend_dict)
    #step5: get sentiment trend----flow_text_es
    sentiment_trend, sentiment_tag_vector = get_attr_sentiment_trend(uid_list)
    results = dict(results, **sentiment_trend)
    tag_vector_result = dict(tag_vector_result, **sentiment_tag_vector)
    #step6: get influence user
    influence_user_result = get_influence_user(uid_list)
    results = dict(results, **influence_user_result)
    #step7: get user sentiment words
    user_sentiment_words = get_attr_sentiment_word(uid_list)
    results = dict(results, **user_sentiment_words)
    results['tag_vector'] = json.dumps(tag_vector_result)
    #step8: get user topic model
    user_topic_results = get_attr_topic_model(uid_list)
    results['topic_model'] = json.dumps(user_topic_results)
    #step8: update compute status to completed
    results['status'] = 1
    #step9: save results
    save_group_results(results)
    #print 'results:', results
    return results


if __name__=='__main__':
    log_time_ts = time.time()
    log_time_date = ts2datetime(log_time_ts)
    print 'cron/group/cron_group.py&start&' + log_time_date
    
    #try:
    compute_group_task_v2()
    #except Exception, e:
    #    print e, '&error&' + ts2date(time.time())

    log_time_ts = time.time()
    log_time_date = ts2datetime(log_time_ts)
    print 'cron/group/cron_group.py&end&' + log_time_date

