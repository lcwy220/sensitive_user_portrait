# -*- coding: utf-8 -*-

import json
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
        "text":{
            "properties":{
                "uid":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "sensitive_words":{
                    "type":"string",
                    "index":"not_analyzed"
                }, # sensitive words dict
                "mid":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "ip":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "timestamp":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "message_type":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "sensitive":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "root_mid":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "text":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "direct_uname":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "direct_uid":{
                    "type": "string",
                    "index": "not_analyzed"
                }
            }
        }
    }
}


es = Elasticsearch('219.224.135.93:9206', timeout=60)

es.indices.create(index="weibo_text", body=index_info, ignore=400)

