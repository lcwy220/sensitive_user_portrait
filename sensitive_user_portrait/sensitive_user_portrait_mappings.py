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
                "sensitive_geo_activity":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "sensitive_geo_string":{
                    "type": "string",
                    "analyzer": "my_analyzer"
                },
                "geo_activity":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "geo_string":{
                    "type": "string",
                    "analyzer": "my_analyzer"
                },
                "sensitive_hashtag_string":{
                    "type": "string",
                    "analyzer": "my_analyzer"
                },
                "sensitive_hashtag_dict":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "hashtag_string":{
                    "type": "string",
                    "analyzer": "my_analyzer"
                },
                "hashtag_dict":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "keywords":{
                    "type": "string",
                    "index": "not_analyzed"
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
                    "index": "not_analyzed"
                },


                "topic_string":{
                    "type": "string",
                    "analyzer": "my_analyzer"
                },

                "importance": {
                    "type": "long"
                },
                "influence": {
                    "type": "long"
                },
                "activeness": {
                    "type": "long"
                },

                "emoticon": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "online_pattern":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "link": {
                    "type": "long",
                    "index": "not_analyzed"
                },
                "fansnum": {
                    "type": "long"
                },
                "text_len": {
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
                "emotion_words": {
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
    es.indices.create(index="sensitive_user_portrait", body=index_info, ignore=400)

