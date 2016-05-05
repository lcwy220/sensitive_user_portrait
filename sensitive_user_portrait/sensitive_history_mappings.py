# -*-coding:utf-8-*-

import sys
import json
from global_utils import ES_CLUSTER_FLOW1 as es

index_info = {
    "mappings":{
        "sensitive":{
            "properties":{
                "sensitive_week_sum":{
                    "type": "double"
                },
                "sensitive_month_sum":{
                    "type": "double"
                },
                "sensitive_day_change":{
                    "type": "double"
                },
                "sensitive_week_change":{
                    "type": "double"
                },
                "sensitive_week_ave":{
                    "type": "double"
                },
                "sensitive_week_var":{
                    "type": "double"
                },
                "sensitive_month_change":{
                    "type": "double"
                },
                "sensitive_month_ave":{
                    "type": "double"
                },
                "sensitive_month_var":{
                    "type": "double"
                }
            }
        }
    }
}

def mappings(index_name):
    exist_bool = es.indices.exists(index=index_name)
    print exist_bool
    if not exist_bool:
        es.indices.create(index=index_name, body=index_info, ignore=400)
        return "1"

if __name__ == "__main__":
    mappings("sensitive_history")
