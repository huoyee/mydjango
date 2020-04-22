ps -ef | grep 'mydjango' | grep 'manage.py' |cut -c 9-15| xargs kill -9
ps -ef | grep 'manage.py' | grep 'beat' |cut -c 9-15 | xargs kill -9
ps -ef | grep 'manage.py' | grep 'worker' | cut -c 9-15 | xargs kill -9
ps -ef | grep 'flower' |grep -v grep | cut -c 9-15 | xargs kill -9
