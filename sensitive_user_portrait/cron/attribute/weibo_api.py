# -*- coding:UTF-8 -*-
import csv
import sys
from elasticsearch import Elasticsearch

reload(sys)
sys.path.append('./../../')
#from text_attribute import attr_liwc


'''
# read from weibo api
def read_user_weibo(uid_list):
    user_weibo_dict = dict()
    return user_weibo_dict
'''
# test: read user weibo
def read_user_weibo(uid_list=[]):
    count = 0
    bulk_action = []
    user_weibo_dict = dict()
    csvfile = open('./sensitive_uid_text.csv', 'rb')
    reader = csv.reader(csvfile)
    for line in reader:
        count += 1
        weibo = dict()
        user = line[0]
        weibo['uname'] = 'unknown'
        weibo['text'] = line[1].decode('utf-8')
        try:
            user_weibo_dict[user].append(weibo)
        except:
            user_weibo_dict[user] = [weibo]

    return user_weibo_dict

if __name__ == '__main__':
    read_user_weibo()
