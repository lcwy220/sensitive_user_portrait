#!/bin/sh
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/scws/lib

cd /home/user_portrait_0320/revised_user_portrait/user_portrait/user_portrait/cron/text_attribute

python scan_compute_redis_imm.py >> /home/log/compute_imm.log

