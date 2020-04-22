#!/bin/bash
conda activate mydjango
cd /home/githup/mydjango

#kill
ps -ef | grep 'mydjango' | grep 'manage.py' |grep -v grep |cut -c 9-15| xargs kill -9
ps -ef | grep 'manage.py' | grep 'beat' |grep -v grep |cut -c 9-15 | xargs kill -9
ps -ef | grep 'manage.py' | grep 'worker' |grep -v grep | cut -c 9-15 | xargs kill -9
ps -ef | grep 'flower' |grep -v grep | cut -c 9-15 | xargs kill -9

#run
nohup python manage.py runserver 139.129.92.179:5000 &
nohup python manage.py celery worker &
nohup python manage.py celery beat &
nohup python manage.py celery flower --address=139.129.92.179 --port=5001