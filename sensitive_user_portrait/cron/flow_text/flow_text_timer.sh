#!/bin/sh
cd /home/ubuntu01/user_portrait/user_portrait/cron/flow_text
tmux kill-session -t flow_text
tmux new-session -s flow_text -d
tmux new-window -n first -t flow_text
tmux new-window -n redis -t flow_text
#python stop_zmq_vent.py >> /home/log/flow2.log
python del_file_yes.py >> /home/log/flow_text.log
tmux send-keys -t flow_text:redis 'python zmq_vent_weibo_flow5.py' C-m
python restart_zmq_vent.py >> /home/log/flow_text.log
