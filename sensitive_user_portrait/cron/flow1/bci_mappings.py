# -*- coding:utf-8 -*-
from elasticsearch import Elasticsearch

index_info = {
    "mappings":{
        "bci":{
            "properties":{
                "uid": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "s_origin_weibo_retweeted_detail":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "s_origin_weibo_comment_detail":{
                    "type": 'string',
                    "index": "not_analyzed"
                },
                "s_retweeted_weibo_retweeted_detail": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "s_retweeted_weibo_comment_detail": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "origin_weibo_retweeted_detail": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                'origin_weibo_comment_detail': {
                    "type": "string",
                    "index": "not_analyzed"
                },
                'retweeted_weibo_retweeted_detail':{
                    "type": "string",
                    "index": "not_analyzed"
                },
                'retweeted_weibo_comment_detail': {
                    "type": "string",
                    "index": "not_analyzed"
                } 
            }
        }
    }
}


def mappings(es, index_name):
    es.indices.create(index=index_name, body=index_info, ignore=400)
    return 1








