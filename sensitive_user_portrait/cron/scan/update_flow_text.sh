#!/bin/sh
tmux kill-session -t update_mid
tmux new-session -s update_mid -d

tmux  new-window -n first -t update_mid
tmux new-window -n redis -t update_mid
tmux new-window -n es1 -t update_mid
tmux new-window -n es2 -t update_mid
tmux new-window -n es3 -t update_mid
#tmux new-window -n es4 -t update_mid

tmux send-keys -t update_mid:redis 'python push_mid2redis.py >> /home/log/update_mid.log' C-m
tmux send-keys -t update_mid:es1 'python update_flow_text.py >> /home/log/update_mid.log' C-m
tmux send-keys -t update_mid:es2 'python update_flow_text.py >> /home/log/update_mid.log' C-m
tmux send-keys -t update_mid:es3 'python update_flow_text.py >> /home/log/update_mid.log' C-m
#tmux send-keys -t update_mid:es4 'python update_flow_text.py >> /home/log/update_mid.log' C-m
