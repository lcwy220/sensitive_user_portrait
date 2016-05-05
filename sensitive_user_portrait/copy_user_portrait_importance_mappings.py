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
        "importance":{
            "properties":{
                "uid":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "importance_week_ave": {
                    "type": "double"
                },
                "importance_week_var": {
                    "type": "double"
                },
                "importance_week_sum": {
                    "type": "double"
                },
                "importance_month_ave": {
                    "type": "double"
                },
                "importance_month_var": {
                    "type": "double"
                },
                "importance_month_sum": {
                    "type": "double"
                },
                "importance_day_change": {
                    "type": "double"
                },
                "importance_month_change": {
                    "type": "double"
                },
                "importance_week_change": {
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
    exist_bool = es.indices.exists(index="copy_user_portrait_importance")
    print exist_bool
    if not exist_bool:
        es.indices.create(index="copy_user_portrait_importance", body=index_info, ignore=400)

