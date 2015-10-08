# -*- coding: UTF-8 -*-
'''
use to save text of users who is supervised
'''
from elasticsearch import Elasticsearch
from global_utils import es_sensitive_user_portrait as es

def main():
    index_info = {
        'settings':{
            'analysis':{
                'analyzer':{
                    'my_analyzer':{
                        'type': 'pattern',
                        'pattern': '&'
                        }
                    }
                }
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
                        'type': 'long'
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
                        },
                    'hashtag':{
                        'type': 'string',
                        'analyzer': 'my_analyzer'
                        },
                    'sensitive_word':{
                        'type': 'string',
                        'analyzer': 'my_analyzer'
                        }

                    }
                }
            }
        }
    es.indices.create(index='monitor_user_text', body=index_info, ignore=400)
    es.index(index='monitor_user_text', doc_type='text', id='test', body={'uid': 'test'})

if __name__=='__main__':
    main()
