# -*-coding:utf-8-*-

import time
import json
import math
from global_utils import es_sensitive_user_portrait as es
from global_utils import es_user_profile, portrait_index_name, portrait_index_type,profile_index_name, profile_index_type

def get_evaluate_max():
    max_result = {}
    evaluate_index = ['activeness', 'importance', 'influence', 'sensitive']
    for evaluate in evaluate_index:
        query_body = {
            "query":{
                'match_all':{}
                },
            "size":1,
            'sort':[{evaluate: {'order': 'desc'}}]
        }
        result = es.search(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)['hits']['hits']
        max_evaluate = result[0]['_source'][evaluate]
        if max_evaluate != 0:
            max_result[evaluate] = max_evaluate
        else:
            max_result[evaluate] = 99999

    return max_result


def normalize_index(index, max_value):
    normal_value = math.log(index/float(max_value)*9+1,10)*100
    return normal_value

def get_user_portrait(uid_list, specify_field=[]):
    if not uid_list:
        return []
    results = []
    max_result = get_evaluate_max()
    fields_list = ['uname','domain','topic_string','politics','fansnum','statusnum','friendsnum','location']
    index_list = ["activeness", 'importance', 'influence', 'sensitive']
    search_results = es.mget(index=portrait_index_name,doc_type=portrait_index_type,body={"ids":uid_list}, _source=False, \
            fields=['uname','domain','topic_string','politics','fansnum','statusnum','friendsnum','location','activeness','importance','influence','sensitive'])["docs"]
    if specify_field:
        fields_list = specify_field
    for item in search_results:
        iter_result = []
        iter_result.append(item['_id'])
        if item['found']:
            for iter_field in fields_list:
                if iter_field == "topic_string":
                    iter_result.append(item['fields'][iter_field][0].split('&'))
                else:
                    iter_result.append(item['fields'][iter_field][0])
            for iter_field in index_list:
                index_value = item['fields'][iter_field][0]
                normal_value = normalize_index(index_value, max_result[iter_field])
                iter_result.append(normal_value)
        else:
            iter_result.extend(['']*12)
        results.append(iter_result)

    return results


def get_user_profile(uid_list,specify_field=[]):
    if not uid_list:
        return []

    results = []
    search_results = es_user_profile.mget(index=profile_index_name, doc_type=profile_index_type,body={"ids":uid_list})['docs']
    field_list = ["nick_name", "fansnum", "friendsnum","photo_url", 'description', "statusnum","sp_type", "user_location", "create_at", "sex", "verified_type", "isreal", "user_email"]
    for item in search_results:
        iter_result = []
        iter_result.append(item['_id'])
        if item['found']:
            if specify_field:
                field_list = specify_field
            for iter_field in field_list:
                iter_result.append(item['_source'][iter_field])
        else:
            iter_result.extend(['']*len(field_list))
        results.append(iter_result)

    return results


if __name__ == "__main__":
    uid_list = ["1109084294", "2319523093", "123456"]
    print get_user_profile(uid_list, ['nick_name'])
    print get_user_portrait(uid_list, ['uname'])
