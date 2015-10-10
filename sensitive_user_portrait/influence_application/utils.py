# -*- coding:utf-8 -*-

import sys
from elasticsearch import Elasticsearch
from sensitive_user_portrait.global_utils import ES_CLUSTER_FLOW1 as es_cluster
from sensitive_user_portrait.global_utils import es_sensitive_user_portrait as es
from sensitive_user_portrait.global_utils import es_user_profile as es_profile


def search_domain(domain, date, number=100):
    # top influence user in domain
    results = {}
    count = 0
    date = str(date).replace('-', '')

    query_body = {
        "query":{
            "match_all": {}
        },
        "sort": {date: {"order": "desc"}},
        "size": 10000
    }

    search_results = es.search(index=date, doc_type='user', body=query_body)['hits']['hits']
    uid_list = []
    for item in search_results:
        domain_list = (item['_source']['domain_string']).split('&')
        if domain in set()



