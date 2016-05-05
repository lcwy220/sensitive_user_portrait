# -*- coding = utf-8 -*-

import os
import time
import sys
reload(sys)
sys.path.append('./../../')
from time_utils import ts2datetime, ts2date
from global_utils import R_SPARK

path = "/home/ubuntu01/txt"
file_list = os.listdir(path)
for each in file_list:
    filename = each.split('.')[0]
    if filename.split('_')[-1] == 'yes3':
        os.remove(path+'/'+each)

R_SPARK.flushdb()
ts = ts2date(time.time())

print "/cron/flow3/del_file_yes.py&end&%s" %ts
print "/cron/flow3/flushdb.py&end&%s" %ts
