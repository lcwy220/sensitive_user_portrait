#!/bin/sh
cd /home/ubuntu01/user_portrait/user_portrait/cron/flow3
tmux kill-session -t flow3
tmux new-session -s flow3 -d
tmux new-window -n first -t flow3
tmux new-window -n redis -t flow3
#python stop_zmq_vent.py >> /home/log/flow2.log
python del_file_yes.py >> /home/log/flow3.log
tmux send-keys -t flow3:redis 'python zmq_vent_weibo_flow3.py' C-m
python restart_zmq_vent.py >> /home/log/flow3.log
