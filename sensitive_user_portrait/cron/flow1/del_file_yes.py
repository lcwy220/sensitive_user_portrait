# -*- coding = utf-8 -*-

import os
import time
import sys
reload(sys)
sys.path.append('./../../')
from time_utils import ts2datetime


path = "/home/ubuntu01/txt"
file_list = os.listdir(path)
for each in file_list:
    filename = each.split('.')[0]
    if filename.split('_')[-1] == 'yes':
        os.remove(path+'/'+each)
ts = ts2datetime(time.time())
print "/cron/flow1/del_file_yes.py&end&%s" %ts
