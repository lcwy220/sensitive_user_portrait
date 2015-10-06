# -*- coding:utf-8 -*-

import sys
import json
from sensitive_user_portrait.global_utils import es_user_profile

writer = ['1311967407', '1195347197', '1142648704', '1889213710', '1706987705']
expert = ['1827652007', '1265965213', '1596329427', '1908195982', '2248789552']
grassroot = ['1220291284', '1635764393', '2682546440', '3188186580', '1665808371']
religion = ['1218353337', '1761179351', '3482911112', '1220291284', '2504433601']
attorney = ['1215031834', '1701401324', '1935084477', '1840604224', '2752172261']
public_intellectual = ['1182389073', '1989660417', '1494720324', '1189591617', '1971861621']
non_public_owner = ['1182391231', '1640571365', '1197161814', '1191220232', '1749127163']
independent_media = ['1189729754', '1497882593', '1742566624', '1661598840', '2283406765']
public_media = ['2803301701', '1974576991', '1639498782', '2105426467', '1644648333']
civil_officer = ['1419517335', '1098736570', '1729736051', '2419062270', '1369714780']
star = ['1687429295', '1195300800', '1997641692', '1746274673', '1223178222']
commonweal = ['3299094722', '1342829361', '1946798710', '1894477791', '1958321657']

search_dict = {'writer': writer, 'expert': expert, 'grassroot': grassroot, 'religion': religion, \
        'attorney': attorney, 'public_intellectual': public_intellectual, 'non_public_owner': non_public_owner, \
        'independent_media': independent_media, 'public_media': public_media, 'civil_officer': civil_officer, \
        'star': star, 'commonweal': commonweal}
index_name = 'weibo_user'
index_type = 'user'

def get_top_user():
    results = dict()
    for domain in search_dict:
        results[domain] = []
        user_list = search_dict[domain]
        profile_result = es_user_profile.mget(index=index_name, doc_type=index_type, body={'ids':user_list})['docs']
        for profile in profile_result:
            uid = profile['_id']
            try:
                uname = profile['_source']['nick_name']
                photo_url = profile['_source']['photo_url']
            except:
                uname = 'unknown'
                photo_url = 'unknown'
            results[domain].append([uid, uname, photo_url])
    return results


