#-*- coding:utf-8 -*-

import os
import time
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from imagine import imagine
from sensitive_user_portrait.global_utils import es_sensitive_user_portrait as es
from sensitive_user_portrait.global_utils import portrait_index_name, portrait_index_type


mod = Blueprint('imagine', __name__, url_prefix='/imagine')
shift_dict = {"sensitive_words": "sensitive_words_string", "hashtag": "hashtag_string"}


@mod.route('/portrait_related/')
def ajax_portrait_related():
    uid = request.args.get('uid', '') # uid
    results = dict()

    if uid:
        portrait_result = es.get(index=portrait_index_name, doc_type=portrait_index_type, id=uid)['_source']
        results["domain"] = portrait_result['domain']
        results["topic"] = portrait_result["topic_string"].replace("&", " ")
        results["politics"] = portrait_result["politics"]
        custom_tag = []
        for key in portrait_result:
            if "tag-" in key:
                tag_value = portrait_result[key]
                temp_list = key.split("-")
                key = temp_list[1:]
                custom_string = key + "-" + tag_value
                custom_tag.append([key, tag_value])
        if custom_tag:
            results["tag_detail"] = custom_tag
            results["tag_string"] = custom_string
        else:
            results["tag_detail"] = []
            results["tag_string"] = ""
        sensitive_words_dict = json.loads(portrait_result["sensitive_words_dict"])
        if sensitive_words_dict:
            sorted_sensitive_words = sorted(sensitive_words_dict.items(), key=lambda x:x[1], reverse=True)
            tmp = sorted_sensitive_words[:3]
            sensitive_words_list = [item[0] for item in tmp]
            results["sensitive_words_string"] = " ".join(sensitive_words_list)
            results["sensitive_words_detail"] = sorted_sensitive_words
        else:
            results["sensitive_words_string"] = ""
            results["sensitive_words_detail"] = []
        keywords_dict = json.loads(portrait_result["keywords_dict"])
        results["keywords_detail"] = keywords_dict
        if keywords_dict:
            tmp = keywords_dict[:3]
            keywords_list = [item[0] for item in tmp]
            results["keywords_string"] = " ".join(keywords_list)
        else:
            results["keywords_string"] = ""
        activity_geo_dict = json.loads(portrait_result["activity_geo_dict"])
        geo_dict = {}
        for item in activity_geo_dict:
            for k, v in item.iteritems():
                if geo_dict.has_key(k):
                    geo_dict[k] += v
                else:
                    geo_dict[k] = v
        if geo_dict:
            sorted_geo_dict = sorted(geo_dict.items(), key=lambda x:x[1], reverse=True)
            results["geo_activity"] = sorted_geo_dict[0][0]
            results["geo_activity_detail"] = sorted_geo_dict
        else:
            results["geo_activity"] = ""
            results["geo_activity_detail"] = []
        hashtag_dict = json.loads(portrait_result["hashtag_dict"])
        sorted_hashtag_dict = sorted(hashtag_dict.items(), key=lambda x:x[1], reverse=True)
        if sorted_hashtag_dict:
            results["hashtag"] = sorted_hashtag_dict[0][0]
            results["hashtag_detail"] = sorted_hashtag_dict
        else:
            results["hashtag"] = ""
            results["hashtag_detail"] = []

    return json.dumps(results)



# politics, sensitive_words_string, domain, topic_string, hashtag_string, activity_geo,keywords_string, tag
@mod.route('/imagine/')
def ajax_imagine():
    uid = request.args.get('uid', '') # uid
    query_keywords = request.args.get('keywords','') # query dict and corresponding weight
    query_weight = request.args.get('weight','')
    size = request.args.get('size', 100)
    keywords_list = query_keywords.split(',')
    weight_list = query_weight.split(',')

    if len(keywords_list) != len(weight_list):
        return json.dumps([])

    query_fields_dict = {}
    for i in range(len(keywords_list)):
        if weight_list[i]:
            query_fields_dict[keywords_list[i]] = int(weight_list[i])

    query_fields_dict['size'] = int(size)
    if uid and query_fields_dict:
        result = imagine(uid, query_fields_dict)
    if result:
        return json.dumps(result)

    return json.dumps([])


