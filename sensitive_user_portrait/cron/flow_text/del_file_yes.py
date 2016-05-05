# -*- coding = utf-8 -*-

import os
import time
import sys
reload(sys)
sys.path.append('../../')
from time_utils import ts2datetime

path = "/home/ubuntu01/txt"
file_list = os.listdir(path)
for each in file_list:
    filename = each.split('.')[0]
    if filename.split('_')[-1] == 'yes5':
        os.remove(path+'/'+each)
ts = time.time()
ts = ts2datetime(ts)
print "/cron/flow_text/del_yes_files&end&%s" %str(ts)
