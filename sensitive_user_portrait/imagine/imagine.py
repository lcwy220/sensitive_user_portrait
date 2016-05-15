# -*- coding:utf-8 -*-

import sys
import json
import math
from elasticsearch import Elasticsearch
from sensitive_user_portrait.global_utils import es_user_portrait as es
from sensitive_user_portrait.global_utils import portrait_index_name, portrait_index_type
from sensitive_user_portrait.global_utils import R_ADMIN

#use to get evaluate max
def get_evaluate_max():
    max_result = {}
    evaluate_index = ['influence', 'activeness', 'importance', 'sensitive']
    for evaluate in evaluate_index:
        query_body = {
            'query':{
                'match_all':{}
                    },
                'size':1,
                'sort':[{evaluate: {'order': 'desc'}}]
                }
        try:
            result = es.search(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)['hits']['hits']
        except Exception, e:
            raise e
        max_evaluate = result[0]['_source'][evaluate]
        max_result[evaluate] = max_evaluate
    return max_result


def imagine(uid, query_fields_dict,index_name=portrait_index_name, doctype=portrait_index_type):
    default_setting_dict = query_fields_dict
    print query_fields_dict

    personal_info = es.get(index=portrait_index_name, doc_type=portrait_index_type, id=uid, _source=True)['_source']

    # tag
    tag_dict = dict()
    tag_dict_value = 0
    if "tag" in query_fields_dict:
        tag_dict_value = query_fields_dict["tag"]
        query_fields_dict.pop("tag")
        for key,value in personal_info.iteritems():
            if "tag-" in key:
                tag_dict[key] = value
    print tag_dict, tag_dict_value

    # size
    sort_size = query_fields_dict["size"]
    query_fields_dict.pop("size")

    keys_list = []
    for k, v in query_fields_dict.iteritems():
        if v:
            keys_list.append(k) #需要进行关联的键

    search_dict = {} # 检索的属性字典
    iter_list = []
    tag_attri_vaule = []

    # 对搜索的键值进行过滤，去掉无用的键
    for iter_key in keys_list:
        if iter_key in personal_info:
            if not personal_info[iter_key] or not query_fields_dict[iter_key]:
                query_fields_dict.pop(iter_key)
                continue
            else:
                iter_list.append(iter_key)
                temp = personal_info[iter_key]
                search_dict[iter_key] = temp.split('&')

            """
            query_fields_dict.pop(iter_key)
            if tag_dict.get(iter_key,''):
                tag_attri_vaule.append(iter_key+"-"+tag_dict[iter_key])
            """

    if len(iter_list) == 0 and len(tag_dict) == 0:
        return []

    query_body = {
        'query':{
            'function_score':{
                'query':{
                    'bool':{
                        'must':[
                        ]
                    }
                }
            }
        }
    }

    number = es.count(index=index_name, doc_type=doctype, body=query_body)['count']
    query_body["size"] = sort_size+100

    for (k,v) in query_fields_dict.items():
        temp = {}
        temp_list = []
        if k in personal_info and v != 0:
            for iter_key in search_dict[k]:
                temp_list.append({'wildcard':{k:{'wildcard':'*'+iter_key+'*', 'boost': v}}})

            query_body['query']['function_score']['query']['bool']['must'].append({'bool':{'should':temp_list}})

    if tag_dict and tag_dict_value:
        temp_list = []
        for k,v in tag_dict.iteritems():
            temp = {"term":{k:v}}
            temp_list.append(temp)
        query_body['query']['function_score']['query']['bool']['must'].append({'bool':{'should':temp_list}})

    result = es.search(index=index_name, doc_type=doctype, body=query_body)['hits']['hits']
    field_list = ['uid','uname', 'activeness','importance', 'influence', 'sensitive']
    evaluate_index_list = ['activeness', 'importance', 'influence', 'sensitive']
    return_list = []
    count = 0

    if len(result) > 1 and result:
        if result[0]['_id'] != uid:
            top_score = result[0]['_score']
        else:
            top_score = result[1]['_score']

    #get evaluate max to normal
    evaluate_max_dict = get_evaluate_max()
    for item in result:
        if uid == item['_id']:
            score = item['_score']
            continue
        info = []
        for field in field_list:
            if field in evaluate_index_list:
                value = item['_source'][field]
                normal_value = math.log(value / float(evaluate_max_dict[field] )* 9 + 1, 10) * 100
            else:
                normal_value = item['_source'][field]
                if not normal_value:
                    normal_value = item['_id']
            info.append(normal_value)
        info.append(item['_score']/float(top_score)*100)
        return_list.append(info)
        count += 1

        if count == sort_size:
            break

    return_list.append(number)

    temp_list = []
    for field in field_list:
        if field in evaluate_index_list:
            value = personal_info[field]
            normal_value = math.log(value / float(evaluate_max_dict[field]) * 9 + 1, 10) * 100
        else:
            normal_value = personal_info[field]
        temp_list.append(normal_value)

    results = []
    results.append(temp_list)
    results.extend(return_list)


    return results




if __name__ == '__main__':
    print imagine(2010832710, {'topic':1, 'keywords':2,'field':'default','size':11}, index_name='test_user_portrait', doctype='user')

