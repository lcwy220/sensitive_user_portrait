# -*- coding: UTF-8 -*-

import sys
reload(sys)
sys.path.append('../../')
from global_utils import ES_CLUSTER_FLOW2 as es_cluster

activity_info = {
    "mappings":{
        "activity":{
            "properties":{
                "uid":{
                    "type":"string",
                    "index":"not_analyzed"
                    },
                "activity_dict":{
                    "type": "string",
                    "index": "no"
                }
            }
        }
    }
}

sensitive_activity_info = {
    "mappings":{
        "sensitive_activity":{
            "properties":{
                "uid":{
                    "type":"string",
                    "index": "not_analyzed"
                },
                "sensitive_activity_dict":{
                    "type": "string",
                    "index": "no"
                }
            }
        }
    }
}



def mapping(index_name, doc_type):
    exist_bool = es_cluster.indices.exists(index=index_name)
    if not exist_bool:
        if doc_type == "activity":
            es_cluster.indices.create(index=index_name, body=activity_info, ignore=400)
        else:
            es_cluster.indices.create(index=index_name, body=sensitive_activity_info, ignore=400)
