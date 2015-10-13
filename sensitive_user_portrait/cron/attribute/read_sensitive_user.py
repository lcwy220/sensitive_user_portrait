# -*- coding: utf-8 -*-
"""
copy es_portrait to a new es, for the use of record user_index

"""

import sys
import time
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

reload(sys)
sys.path.append('./../../')
from global_utils import es_sensitive_user_portrait as es

sensitive_user_portrait = "sensitive_user_portrait"
sensitive_user_portrait_doctype = "user"

def expand_index_action(data):
    _id = data['uid']
    action = {'index': {'_id': _id}}
    return action, data


def read_sensitive_user_portrait():
    tb = time.time()

    index_exist = es.indices.exists(index=sensitive_user_portrait)
    if not index_exist:
        es.indices.create(index=index_destination, ignore=400)

    s_re = scan(es, query={"query":{"match_all":{}},"size":1000}, index=sensitive_user_portrait, doc_type=sensitive_user_portrait_doctype)
    count = 0
    user_set = set()
    bulk_action = []
    while 1:
        try:
            scan_re = s_re.next()['_source']['uid']
            #scan_re = s_re.next()['_source']
            #xdata = expand_index_action(scan_re)
            #bulk_action.extend([xdata[0], xdata[1]])
            count += 1
            user_set.add(scan_re)
            #if count % 500 == 0:
            #    es.bulk(bulk_action, index='test_sensitive_user_portrait', doc_type='user', timeout=30)
            #    bulk_action = []
        except StopIteration:
            print "all done"
            break
        except Exception, r:
            print Exception, r
            sys.exit(0)
    #if bulk_action:
    #    es.bulk(bulk_action, index='test_sensitive_user_portrait', doc_type='user', timeout=30)
    print count

    return user_set

if __name__ == "__main__":
    print read_sensitive_user_portrait()
