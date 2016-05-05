# -*- coding: UTF-8 -*-

import sys
reload(sys)
sys.path.append('../../')
from global_utils import ES_CLUSTER_FLOW2 as es_cluster

ip_info = {
    "mappings":{
        "ip":{
            "properties":{
                "uid":{
                    "type":"string",
                    "index":"not_analyzed"
                    },
                "ip_dict":{
                    "type": "string",
                    "index": "no"
                }
            }
        }
    }
}

sensitive_ip_info = {
    "mappings":{
        "sensitive_ip":{
            "properties":{
                "uid":{
                    "type":"string",
                    "index": "not_analyzed"
                },
                "sensitive_ip_dict":{
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
        if doc_type == "ip":
            es_cluster.indices.create(index=index_name, body=ip_info, ignore=400)
        else:
            es_cluster.indices.create(index=index_name, body=sensitive_ip_info, ignore=400)
