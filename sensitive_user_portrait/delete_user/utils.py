# -*-coding:utf-8-*-

from sensitive_user_portrait.global_utils import es_sensitive_user_portrait as es
from elasticsearch import Elasticsearch

def get_user_info(uid_list):
    results = {}
    search_results = es.mget(index='sensitive_user_portrait', doc_type='user', body={'ids':uid_list})['docs']
    fields = ['uid', 'uname', 'domain', 'sensitive', 'importance', 'influence', 'activeness']
    for item in search_results:
        detail = []
        for field in fields:
            detail.append(item['_source'][field])
        results[item['_id']] = detail

    return results




