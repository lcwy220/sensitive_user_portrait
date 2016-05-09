# -*- coding: utf-8 -*-

import json
from global_utils import es_sensitive_user_portrait as es
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

index_info = {
    "settings":{
        "analysis":{
            "analyzer":{
                "my_analyzer":{
                    "type": "pattern",
                    "pattern": "&"
                }
            }
        }
    },

    "mappings":{
        "user":{
            "properties":{
                "domain":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "domain_list":{
                    "type": "string",
                    "index": "no"
                },
                "politics":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "sensitive_words_dict":{
                    "type":"string",
                    "index":"not_analyzed"
                }, # sensitive words dict
                "sensitive_words_string":{
                    "type":"string",
                    "analyzer": "my_analyzer"
                }, # & linked
                "uname":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "uid":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "sensitive_activity_geo_dict":{
                    "type": "string",
                    "index": "no"
                },
                "sensitive_activity_geo":{
                    "type": "string",
                    "analyzer": "my_analyzer"
                },
                "sensitive_activity_geo_aggs":{
                    "type": "string",
                    "analyzer": "my_analyzer"
                },
                # 所有地点检索
                "activity_geo":{
                    "type": "string",
                    "analyzer": "my_analyzer"
                },
                # 地理轨迹
                "activity_geo_dict":{
                    "type": "string",
                    "index": "no"
                },
                # 最后一个位置检索
                "activity_geo_aggs":{
                    "type": "string",
                    "analyzer": "my_analyzer"
                },
                "sensitive_hashtag_string":{
                    "type": "string",
                    "analyzer": "my_analyzer"
                },
                "sensitive_hashtag_dict":{
                    "type": "string",
                    "index": "no"
                },
                "hashtag_string":{
                    "type": "string",
                    "analyzer": "my_analyzer"
                },
                "hashtag_dict":{
                    "type": "string",
                    "index": "no"
                },
                "keywords_dict":{
                    "type": "string",
                    "index": "no"
                },
                "keywords_string":{
                    "type" : "string",
                    "analyzer": "my_analyzer"
                },
                "psycho_status_string":{
                    "type" : "string",
                    "analyzer": "my_analyzer"
                },
                "psycho_status":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "topic":{
                    "type": "string",
                    "index": "no"
                },
                "topic_string":{
                    "type": "string",
                    "analyzer": "my_analyzer"
                },

                "importance": {
                    "type": "float"
                },
                "influence": {
                    "type": "float"
                },
                "activeness": {
                    "type": "float"
                },
                "sensitive": {
                    "type": "float"
                },

                "online_pattern":{
                    "type": "string",
                    "index": "no"
                },
                "online_pattern_aggs":{
                    "type":"string",
                    "analyzer": "my_analyzer"
                },
                "fansnum": {
                    "type": "long"
                },
                "photo_url": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "verified": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "statusnum": {
                    "type": "long"
                },
                "gender": {
                    "type": "long"
                },
                "location": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "friendsnum": {
                    "type": "long"
                }
            }
        }
    }
}

exist_bool = es.indices.exists(index="sensitive_user_portrait")
if not exist_bool:
    print "not exist"
    print es.indices.create(index="sensitive_user_portrait", body=index_info, ignore=400)

