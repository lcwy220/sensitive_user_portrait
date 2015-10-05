# -*- coding: UTF-8 -*-
'''
use to save text of users who is supervised
'''
from elasticsearch import Elasticsearch
from global_utils import es_sensitive_user_portrait as es

def main():
    index_info = {
        'settings':{
            'number_of_shards':5,
            'number_of_replicas':0,
            },
        'mappings':{
            'text':{
                'properties':{
                    'text':{
                        'type': 'string',
                        'index': 'not_analyzed'
                        },
                    'mid':{
                        'type': 'string',
                        'index': 'not_analyzed'
                        },
                    'ip':{
                        'type': 'string',
                        'index': 'not_analyzed'
                        },
                    'timestamp':{
                        'type': 'int'
                        },
                    'sentiment':{
                        'type': 'string',
                        'index': 'not_analyzed'
                        },
                    'geo':{
                        'type': 'string',
                        'index': 'not_analyzed'
                        },
                    'message_type':{
                        'type': 'string',
                        'index': 'not_analyzed'
                        },
                    'uid':{
                        'type': 'string',
                        'index': 'not_analyzed'
                        }
                    }
                }
            }
        }
    es.indices.create(index='monitor_user_text', body=index_info, ignore=400)
    es.index(index='monitor_user_text', doc_type='text', id='test', body={'uid': 'test'})

if __name__=='__main__':
    main()
