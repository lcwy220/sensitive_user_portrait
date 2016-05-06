#-*-coding=utf-8-*-
#vision2
import os
import re
import sys
import json
import csv
import random
from find_users import get_friends, get_user
from domain_by_text import domain_classfiy_by_text
from domain_by_des import domain_classify_by_des
from global_utils_do import labels,zh_labels,txt_labels,train_users

def user_domain_classifier_v1(friends, fields_value=txt_labels, protou_dict=train_users):#根据用户的粉丝列表对用户进行分类
    mbr = {'writer':0, 'professor':0, 'root':0, 'religion':0, 'lawyer':0, 'well-known':0, 
          'non-public':0, 'media':0, 'official-media':0, 'governer':0, 'star':0, 'other':0, 'business':0}
   
    # to record user with friends in proto users

    if len(friends) == 0:
         mbr['other'] += 1
    else:
        for area in fields_value:
            c_set = set(friends) & set(protou_dict[area])
            mbr[area] = len(c_set)
     
    count = 0
    count = sum([v for v in mbr.values()])

    if count == 0:
        return ['other']
    
    sorted_mbr = sorted(mbr.iteritems(), key=lambda (k, v): v, reverse=True)
    field1 = [sorted_mbr[0][0],sorted_mbr[1][0],sorted_mbr[2][0]]

    return field1

def getFieldFromProtou(uid, protou_dict=train_users):#判断一个用户是否在种子列表里面

    result = []
    for k,v in protou_dict.iteritems():
        if uid in v:
            result.append(k)

    return result

def get_label(label1,label2,label3):

    label = []
    len1 = len(label1)
    len2 = len(label2)
    len3 = len(label3)
    if len1 > 1 and len2 > 1 and len3 > 1:
        label_dict = dict()
        for i in range(0,3):
            if label_dict.has_key(label1[i]):
                label_dict[label1[i]] = label_dict[label1[i]] + 1
            else:
                label_dict[label1[i]] = 1

            if label_dict.has_key(label2[i]):
                label_dict[label2[i]] = label_dict[label2[i]] + 1
            else:
                label_dict[label2[i]] = 1

            if label_dict.has_key(label3[i]):
                label_dict[label3[i]] = label_dict[label3[i]] + 1
            else:
                label_dict[label3[i]] = 1

        sorted_mbr = sorted(label_dict.iteritems(), key=lambda (k, v): v, reverse=True)
        label = [sorted_mbr[0][0],sorted_mbr[1][0],sorted_mbr[2][0]]
    elif len1 == 1 and len2 > 1 and len3 > 1:
        label_dict = dict()
        for i in range(0,3):
            if label_dict.has_key(label2[i]):
                label_dict[label2[i]] = label_dict[label2[i]] + 1
            else:
                label_dict[label2[i]] = 1

            if label_dict.has_key(label3[i]):
                label_dict[label3[i]] = label_dict[label3[i]] + 1
            else:
                label_dict[label3[i]] = 1

        sorted_mbr = sorted(label_dict.iteritems(), key=lambda (k, v): v, reverse=True)
        label = [sorted_mbr[0][0],sorted_mbr[1][0],sorted_mbr[2][0]]

    elif len1 > 1 and len2 == 1 and len3 > 1:
        label_dict = dict()
        for i in range(0,3):
            if label_dict.has_key(label1[i]):
                label_dict[label1[i]] = label_dict[label1[i]] + 1
            else:
                label_dict[label1[i]] = 1

            if label_dict.has_key(label3[i]):
                label_dict[label3[i]] = label_dict[label3[i]] + 1
            else:
                label_dict[label3[i]] = 1

        sorted_mbr = sorted(label_dict.iteritems(), key=lambda (k, v): v, reverse=True)
        label = [sorted_mbr[0][0],sorted_mbr[1][0],sorted_mbr[2][0]]
    elif len1 > 1 and len2 > 1 and len3 == 1:
        label_dict = dict()
        for i in range(0,3):
            if label_dict.has_key(label1[i]):
                label_dict[label1[i]] = label_dict[label1[i]] + 1
            else:
                label_dict[label1[i]] = 1

            if label_dict.has_key(label2[i]):
                label_dict[label2[i]] = label_dict[label2[i]] + 1
            else:
                label_dict[label2[i]] = 1

        sorted_mbr = sorted(label_dict.iteritems(), key=lambda (k, v): v, reverse=True)
        label = [sorted_mbr[0][0],sorted_mbr[1][0],sorted_mbr[2][0]]
    elif len1 > 1 and len2 == 1 and len3 == 1:
        label = label1
    elif len1 == 1 and len2 > 1 and len3 == 1:
        label = label2
    elif len1 == 1 and len2 == 1 and len3 > 1:
        label = label3
    else:
        label = ['other']

    return label

def get_recommend_result(v_type,label1,label2,label3):#根据三种分类结果选出一个标签

    label = []
    if v_type == 'other':#认证类型字段走不通

        label = get_label(label1,label2,label3)

    else:
        if v_type == 1:#政府
            label_r = get_label(label1,label2,label3)
            if 'other' in label_r:
                label = ['governer']
            else:
                if 'governer' not in label_r:
                    label = ['governer',label_r[0],label_r[1]]
            
        elif v_type == 3:#媒体

            label = get_label(label1,label2,label3)

        elif v_type == 2 or v_type == 5 or v_type == 6 or v_type == 7:
            label = ['other']

        else:
            label = get_label(label1,label2,label3)

    return label            

def domain_classfiy(uid_list,uid_weibo):#领域分类主函数
    '''
    用户领域分类主函数
    输入数据示例：
    uid_list:uid列表 [uid1,uid2,uid3,...]
    uid_weibo:分词之后的词频字典  {uid1:{'key1':f1,'key2':f2...}...}

    输出数据示例：
    domain：标签字典  {uid1:[label1,label2,label3...],uid2:[label1,label2,label3...]...}

    '''
    if not len(uid_weibo) and len(uid_list):
        domain = dict()
        r_domain = dict()
        for uid in uid_list:
            domain[uid] = ['other']
            r_domain[uid] = ['other']
        return domain,r_domain
    elif len(uid_weibo) and not len(uid_list):
        uid_list = uid_weibo.keys()
    elif not len(uid_weibo) and not len(uid_list):
        domain = dict()
        r_domain = dict()
        return domain,r_domain
    else:
        pass
    
    users = get_user(uid_list)
    frineds = get_friends(uid_list)

    domain = dict()
    r_domain = dict()
    text_result = dict()
    user_result = dict()
    for k,v in users.iteritems():

        uid = k
        r = v
        field1 = getFieldFromProtou(k, protou_dict=train_users)#判断uid是否在种子用户里面，返回一个list
        if len(field1):#该用户在种子用户里面
            domain[str(uid)] = field1
        else:
            f = frineds[k]#返回用户的粉丝列表
            if len(f):
                field1 = user_domain_classifier_v1(f, fields_value=txt_labels, protou_dict=train_users)#根据关注关系分类，返回一个list
            else:
                field1 = ['other']

            if r == 'other':
                #field2 = 'other'
                field_d = ['other']
            else:
                #field2 = user_domain_classifier_v2(r)#根据认证类型分类，返回一个标签
                field_dict = domain_classify_by_des({k: v['description']})#根据个人描述分类，返回一个list
                field_d = field_dict[k]

            if uid_weibo.has_key(k) and len(uid_weibo[k]):
                field_dict = domain_classfiy_by_text({k: uid_weibo[k]})#根据用户文本进行分类，返回一个list
                field3 = field_dict[k]
            else:
                field3 = ['other']
            
            if r == 'other':
                re_label = get_recommend_result('other',field1,field_d,field3)#没有认证类型字段
            else:
                re_label = get_recommend_result(r['verified_type'],field1,field_d,field3)
        
            domain[str(uid)] = re_label
    
    return domain

if __name__ == '__main__':
    uid_list,uid_weibo = input_data()
    uid_weibo = dict()
    domain,r_domain = domain_classfiy(uid_list,uid_weibo)
    print domain
    #print r_domain


    
