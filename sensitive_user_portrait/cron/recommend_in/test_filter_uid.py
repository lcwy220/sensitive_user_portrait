# -*- coding=utf-8 -*-

import sys
from elasticsearch import Elasticsearch
reload(sys)
sys.path.append('../../')
from global_utils import ES_CLUSTER_FLOW1 as es_cluster

def search_sensitive_weibo(index_name):
    query_body={
        "query":{
            "match_all":{}
        },
        "sort":{'s_origin_weibo_comment_top_number':{"order": "desc"}},
        "size":2000
    }

    result = es_cluster.search(index=index_name, doc_type="bci", body=query_body)['hits']['hits']
    sensitive_uid = []
    for item in result:
        sensitive_uid.append(item['_source']['uid'])

    return sensitive_uid

if __name__ == '__main__':
    f = open('sensitive_uid_list.txt', 'wb')
    uid_list = search_sensitive_weibo('20130904')
    for uid in uid_list:
        f.write(str(uid) + '\n')
    f.close()
