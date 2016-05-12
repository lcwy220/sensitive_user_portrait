#!/bin/sh

python copy_user_portrait_activeness.py >> /home/log/copy_activeness.log
python copy_user_portrait_influence.py >> /home/log/copy_influence.log
python copy_user_portrait_importance.py >> /home/log/copy_importance.log
python copy_user_portrait_sensitive.py >> /home/log/copy_sensitive.log
