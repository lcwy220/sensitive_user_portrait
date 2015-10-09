# -*- coding: utf-8 -*-

import csv
import os
import sys
import time
from DFA_filter import sensitive_words_extract

reload(sys)
sys.path.append('./../flow1/')
from csv2json import itemLine2Dict, csv2bin
sys.setdefaultencoding('utf-8')

CSV_FILE_PATH = '/home/ubuntu8/data1309/20130901'
uid_csv_path = './../recommend_in/'
uid_csv = 'sensitive_uid_list.txt'

count_n = 0
tb = time.time()
uid_set = set()
with open (os.path.join(uid_csv_path, uid_csv), 'rb') as t:
    for line in t:
        uid = line.strip()
        uid_set.add(uid)
        count_n += 1

uid_text = file('sensitive_uid_text_2.csv', 'wb')
writer = csv.writer(uid_text)
count = 0
count_f = 0

file_list = set(os.listdir(CSV_FILE_PATH))
print "total file is ", len(file_list)

for each in file_list:
    with open(os.path.join(CSV_FILE_PATH, each), 'rb') as f:
        try:
            for line in f:
                count_f += 1
                weibo_item = itemLine2Dict(line)
                if weibo_item:
                    weibo_item_bin = csv2bin(weibo_item)
                    if int(weibo_item_bin['sp_type']) != 1:
                        continue
                    if not str(weibo_item_bin['uid']) in uid_set:
                        continue
                    text = weibo_item_bin['text']
                    message_type = 0
                    if weibo_item_bin['message_type'] == 1:
                        write_text = text
                        message_type = 1
                    elif weibo_item_bin['message_type'] == 2:
                        temp = text.split('//@')[0].split(':')[1:]
                        write_text = ''.join(temp)
                        message_type = 2
                    elif weibo_item_bin['message_type'] == 3:
                        write_text = text
                        message_type = 3
                    else:
                        continue
                    if not isinstance(write_text, str):
                        text = text.encode('utf-8', 'ignore')
                    if text:
                        sw_dict = sensitive_words_extract(text)
                        if not sw_dict:
                            sensitive = 0
                        else:
                            seneitive = 1
                    item = [str(weibo_item_bin['uid']), write_text, str(weibo_item_bin['mid']), str(weibo_item_bin['send_ip']), str(weibo_item_bin['timestamp']), message_type, sensitive ]

                    if write_text != "":
                        writer.writerow(item)
                        count += 1

                if count_f % 10000 == 0:
                    ts = time.time()
                    print "%s  per  %s  second" %(count_f, ts-tb)
                    print "have get %s" % count
                    tb = ts
        except SystemError:
            print "system error"

        except Exception, r:
            print Exception, r


