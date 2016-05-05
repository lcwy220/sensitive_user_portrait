# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
from global_utils import ES_CLUSTER_FLOW1 as es

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
        "sensitive":{
            "properties":{
                "uid":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "sensitive_week_ave": {
                    "type": "double"
                },
                "sensitive_week_var": {
                    "type": "double"
                },
                "sensitive_week_sum": {
                    "type": "double"
                },
                "sensitive_month_ave": {
                    "type": "double"
                },
                "sensitive_month_var": {
                    "type": "double"
                },
                "sensitive_month_sum": {
                    "type": "double"
                },
                "sensitive_day_change": {
                    "type": "double"
                },
                "sensitive_month_change": {
                    "type": "double"
                },
                "sensitive_week_change": {
                    "type": "double"
                },
                "domain": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "hashtag":{
                    "type": "string",
                    "analyzer": "my_analyzer"
                },
                "topic_string":{
                    "type": "string",
                    "analyzer": "my_analyzer"
                },
                "activity_geo":{
                    "type": "string",
                    "analyzer": "my_analyzer"
                }
            }
        }
    }
}


if __name__ == "__main__":
    exist_bool = es.indices.exists(index="copy_user_portrait_sensitive")
    print exist_bool
    if not exist_bool:
        es.indices.create(index="copy_user_portrait_sensitive", body=index_info, ignore=400)

