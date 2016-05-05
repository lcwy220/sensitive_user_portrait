#-*- coding: utf-8 -*-

import redis
from elasticsearch import Elasticsearch
from global_config import REDIS_HOST_INFLUENCE, REDIS_PORT_INFLUENCE, REDIS_HOST_IP, REDIS_PORT_IP, \
                          REDIS_HOST_ACTIVITY, REDIS_PORT_ACTIVITY, REDIS_HOST_CLUSTER, REDIS_PORT_CLUSTER, \
                          REDIS_HOST_RETWEET, REDIS_PORT_RETWEET, REDIS_HOST_COMMENT, REDIS_PORT_COMMENT, \
                          UNAME2UID_HOST, UNAME2UID_PORT, UNAME2UID_HASH, REDIS_HOST, REDIS_PORT, MONITOR_REDIS_HOST, MONITOR_REDIS_PORT
from global_config import USER_PROFILE_ES_HOST, USER_PROFILE_ES_PORT, \
                          SENSITIVE_USER_PORTRAIT_ES_HOST, SENSITIVE_USER_PORTRAIT_ES_PORT,REDIS_TEXT_MID_HOST, REDIS_TEXT_MID_PORT, \
                          FLOW_TEXT_ES_HOST, FLOW_TEXT_ES_PORT, ES_CLUSTER_HOST_FLOW1, ES_CLUSTER_HOST_FLOW2
from parameter import RUN_TYPE

redis_influence = redis.StrictRedis(host=REDIS_HOST_INFLUENCE, port=REDIS_PORT_INFLUENCE, db=0)
redis_ip = redis.StrictRedis(host=REDIS_HOST_IP, port=REDIS_PORT_IP, db=0)
redis_activity = redis.StrictRedis(host=REDIS_HOST_ACTIVITY, port=REDIS_PORT_ACTIVITY, db=0)
redis_cluster = redis.StrictRedis(host=REDIS_HOST_CLUSTER, port=REDIS_PORT_CLUSTER)
redis_retweet_1 = redis.StrictRedis(host=REDIS_HOST_RETWEET, port=REDIS_PORT_RETWEET, db=1)
redis_retweet_2 = redis.StrictRedis(host=REDIS_HOST_RETWEET, port=REDIS_PORT_RETWEET, db=2)
redis_comment_1 = redis.StrictRedis(host=REDIS_HOST_COMMENT, port=REDIS_PORT_COMMENT, db=1)
redis_comment_2 = redis.StrictRedis(host=REDIS_HOST_COMMENT, port=REDIS_PORT_COMMENT, db=2)
sensitive_redis_retweet_1 = redis.StrictRedis(host=REDIS_HOST_RETWEET, port=REDIS_PORT_RETWEET, db=3)
sensitive_redis_retweet_2 = redis.StrictRedis(host=REDIS_HOST_RETWEET, port=REDIS_PORT_RETWEET, db=4)
sensitive_redis_comment_1 = redis.StrictRedis(host=REDIS_HOST_COMMENT, port=REDIS_PORT_COMMENT, db=3)
sensitive_redis_comment_2 = redis.StrictRedis(host=REDIS_HOST_COMMENT, port=REDIS_PORT_COMMENT, db=4)
redis_host_list = ["1", "2"]
sensitive_redis_host_list = ["3", "4"]
retweet_redis_dict = {'1':redis_retweet_1, '2':redis_retweet_2}
comment_redis_dict = {'1':redis_comment_1, '2':redis_comment_2}
sensitive_retweet_redis_dict = {'3':redis_retweet_1, '4':redis_retweet_2}
sensitive_comment_redis_dict = {'3':redis_comment_1, '4':redis_comment_2}
redis_admin = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=15)
uname2uid_redis = redis.StrictRedis(host=UNAME2UID_HOST, port=UNAME2UID_PORT)


def _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=0):
    return redis.StrictRedis(host, port, db)
redis_flow_text_mid = _default_redis(host=REDIS_TEXT_MID_HOST, port=REDIS_TEXT_MID_PORT, db=2)

R_RECOMMENTATION = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=12)

R_RECOMMENTATION_OUT = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=12)

R_ADMIN = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=12)


update_day_redis = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=6)
UPDATE_DAY_REDIS_KEY = 'update_day'
update_week_redis  = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=6)
UPDATE_WEEK_REDIS_KEY = 'update_week'
update_month_redis = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=6)
UPDATE_MONTH_REDIS_KEY = 'update_month'

#use to keep the track task queue
R_GROUP_TASK = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=13)

# use to keep the track task user·
R_GROUP = _default_redis(host=REDIS_HOST, port=REDIS_PORT, db=14)
# use to save monitor user be_retweet and be_count result
MONITOR_REDIS = _default_redis(host=MONITOR_REDIS_HOST, port=MONITOR_REDIS_PORT, db=1)
# use to save monitor user inner group retweet
MONITOR_INNER_REDIS = _default_redis(host=MONITOR_REDIS_HOST, port=MONITOR_REDIS_PORT, db=2)

def get_db_num(timestamp):
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    db_number = (((date_ts - r_begin_ts) / DAY) / 7) % 2 + 1
    if RUN_TYPE == 0:
        db_number = 1
    return db_number


# elasticsearch initialize, one for user_profile, one for user_portrait
es_user_profile = Elasticsearch(USER_PROFILE_ES_HOST, timeout = 600)
es_sensitive_user_portrait = Elasticsearch(SENSITIVE_USER_PORTRAIT_ES_HOST, timeout=600)
ES_COPY_USER_PORTRAIT = Elasticsearch(SENSITIVE_USER_PORTRAIT_ES_HOST, timeout=600)
es_flow_text = Elasticsearch(FLOW_TEXT_ES_HOST, timeout=600)
es_retweet = Elasticsearch(ES_CLUSTER_HOST_FLOW2, timeout = 600)
es_comment = Elasticsearch(ES_CLUSTER_HOST_FLOW2, timeout = 600)
es_copy_portrait = Elasticsearch(SENSITIVE_USER_PORTRAIT_ES_HOST, timeout = 600)
es_tag = Elasticsearch(SENSITIVE_USER_PORTRAIT_ES_HOST, timeout=600)
# bci
ES_CLUSTER_FLOW1 = Elasticsearch(ES_CLUSTER_HOST_FLOW1, timeout=600)
# ip/activity
ES_CLUSTER_FLOW2 = Elasticsearch(ES_CLUSTER_HOST_FLOW2, timeout=600)
es_sensitive_user_text = es_flow_text
es_user_portrait = es_sensitive_user_portrait
es_sensitive_history = Elasticsearch(ES_CLUSTER_HOST_FLOW1, timeout=600)


portrait_index_name = "sensitive_user_portrait"
portrait_index_type = "user"
bci_index_name_pre = "bci_"
bci_index_type = "bci"
flow_text_index_name_pre = "flow_text_"
flow_text_index_type = "text"
profile_index_name = 'weibo_user'
profile_index_type = 'user'
retweet_index_name_pre = 'retweet_'
retweet_index_type = 'user'
be_retweet_index_name_pre = 'be_retweet_'
be_retweet_index_type = 'user'
comment_index_name_pre = 'comment_'
comment_index_type = 'user'
be_comment_index_name_pre = 'be_comment_'
be_comment_index_type = 'user'
sensitive_retweet_index_name_pre = 'sensitive_retweet_'
sensitive_retweet_index_type = 'user'
sensitive_be_retweet_index_name_pre = 'sensitive_be_retweet_'
sensitive_be_retweet_index_type = 'user'
sensitive_comment_index_name_pre = 'sensitive_comment_'
sensitive_comment_index_type = 'user'
sensitive_be_comment_index_name_pre = 'sensitive_be_comment_'
sensitive_be_comment_index_type = 'user'
copy_portrait_index_name = 'copy_sensitive_user_portrait'
copy_portrait_index_type = 'manage'



BLACK_WORDS_PATH = '/home/ubuntu8/yuankun/sensitive_user_portrait/sensitive_user_portrait/cron/text_attribute/black.txt'

def load_black_words():
    black_words = set([line.strip('\r\n') for line in file(BLACK_WORDS_PATH)])
    return black_words

black_words = load_black_words()

ES_SENSITIVE_INDEX = "sensitive_history"
DOCTYPE_SENSITIVE_INDEX = "sensitive"

COPY_USER_PORTRAIT_INFLUENCE = "copy_user_portrait_influence"
COPY_USER_PORTRAIT_INFLUENCE_TYPE = 'bci'
COPY_USER_PORTRAIT_IMPORTANCE = "copy_user_portrait_importance"
COPY_USER_PORTRAIT_IMPORTANCE_TYPE = 'importance'
COPY_USER_PORTRAIT_ACTIVENESS = "copy_user_portrait_activeness"
COPY_USER_PORTRAIT_ACTIVENESS_TYPE = 'activeness'
COPY_USER_PORTRAIT_SENSITIVE = "copy_user_portrait_sensitive"
COPY_USER_PORTRAIT_SENSITIVE_TYPE = 'sensitive'
