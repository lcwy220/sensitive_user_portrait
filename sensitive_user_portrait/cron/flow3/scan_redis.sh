#!/bin/sh
cd /home/ubuntu01/user_portrait/user_portrait/cron/flow3
tmux kill-session -t scan_redis
tmux new-session -s scan_redis -d

tmux new-window -n first -t scan_redis
tmux new-window -n retweet -t scan_redis
tmux new-window -n comment -t scan_redis
tmux send-keys -t scan_redis:comment 'python scan_redis2es_comment.py >> /home/log/scan_redis.log' C-m
tmux send-keys -t scan_redis:retweet 'python scan_redis2es_retweet.py >> /home/log/scan_redis.log' C-m




