# -*- coding: utf-8 -*-

import redis
from elasticsearch import Elasticsearch
from global_config_ys import USER_PORTRAIT_ES_HOST, USER_PORTRAIT_ES_PORT


# elasticsearch initialize, one for user_profile, one for user_portrait
#es_user_profile = Elasticsearch(USER_PROFILE_ES_HOST, timeout = 600)
es_user_profile = Elasticsearch(USER_PORTRAIT_ES_HOST, timeout = 600)
es_retweet = Elasticsearch(USER_PORTRAIT_ES_HOST, timeout = 600)

# elasticsearch index_name and index_type
profile_index_name = 'weibo_user'  # user profile es
profile_index_type = 'user'
# week retweet/be_retweet relation es
retweet_index_name_pre = '1225_retweet_' # retweet: 'retweet_1' or 'retweet_2'
retweet_index_type = 'user'


