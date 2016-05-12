# -*-coding:utf-8-*-
import sys
reload(sys)
sys.path.append('../../')
from global_utils import es_sensitive_user_portrait as es
from global_utils import es_user_profile

domain_list = ['作家写手', '专家学者', '草根红人', '宗教人士', '维权律师', '公知分子', '非公企业主', \
        '独立媒体人', '官方媒体', '公职人员', '文体明星', '社会公益']

topic_list = ['暴恐','邪教','意识形态','民生','宗教']

def query_body(key, value):
    query_body_dict = {
        "query":{
            "filtered":{
                "filter":{
                    "term":{key:value}
                }
            }
        },
        "size":5,
        "sort":{"fansnum":{"order":"desc"}}
    }

    return query_body_dict

def get_top_user():
    results = dict()
    domain_results = dict()
    topic_results = dict()
    for item in domain_list:
        search_query_body = query_body("domain", item)
        search_results = es.search(index="sensitive_user_portrait", doc_type="user", body=search_query_body, _source=False, fields=['uname','photo_url'])['hits']['hits']
        uid_list = []
        for iter_item in search_results:
            uid_list.append([iter_item['_id'], iter_item['fields']['uname'][0], iter_item['fields']['photo_url'][0]])
        domain_results[item] = uid_list


    for item in topic_list:
        search_query_body = query_body("topic_string", item)
        search_results = es.search(index="sensitive_user_portrait", doc_type="user", body=search_query_body, _source=False, fields=['uname','photo_url'])['hits']['hits']
        uid_list = []
        for iter_item in search_results:
            uid_list.append([iter_item['_id'], iter_item['fields']['uname'][0], iter_item['fields']['photo_url'][0]])
        topic_results[item] = uid_list

    results['domain_rank'] = domain_results
    results['topic_rank'] = topic_results

    return results

if __name__ == "__main__":
    print get_top_user()
