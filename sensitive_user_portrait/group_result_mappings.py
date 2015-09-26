# -*- coding:UTF-8 -*-
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from global_utils import es_sensitive_user_portrait as es

index_info = {
    'settings':{
        'number_of_shards':5,
        'number_of_replicas':0,
        },
    'mappings':{
        'group':{
            'properties':{
                'task_name':{
                    'type':'string',
                    'index': 'not_analyzed'
                    },
                'state':{
                    'type':'string',
                    'index': 'not_analyzed'
                    },
                'status':{
                    'type':'long'
                    },
                'submit_date':{
                    'type':'string',
                    'index': 'not_analyzed'
                    }
                }
            }
        }
    }


es.indices.create(index='group_result', body=index_info, ignore=400)

