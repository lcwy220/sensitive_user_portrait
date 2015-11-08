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
            }
        }
    }
}


es = Elasticsearch('219.224.135.93:9206', timeout=60)

es.indices.create(index="weibo_text", body=index_info, ignore=400)

#es.index(index="test_mapping_index", doc_type="user", id="1917335617",body={"uid":"1917335617", "hashtag_string":"中国好声音&急速前进&花千骨", "hashtag":"中国好声音&急速前进&花千骨", "geo_activity":"中国		北京	北京&中国	上海	上海", "geo_activity_string":"北京&上海"})
