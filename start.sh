#!/bin/bash
# vim ~/.bashrc
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/root/anaconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/root/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/root/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/root/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<


conda activate mydjango
cd /home/github/mydjango/

#kill
#ps -ef | grep 'mydjango' | grep 'manage.py' |grep -v grep |cut -c 9-15| xargs kill -9
#ps -ef | grep 'manage.py' | grep 'beat' |grep -v grep |cut -c 9-15 | xargs kill -9
#ps -ef | grep 'manage.py' | grep 'worker' |grep -v grep | cut -c 9-15 | xargs kill -9
#ps -ef | grep 'flower' |grep -v grep | cut -c 9-15 | xargs kill -9

#run
nohup python manage.py runserver 0.0.0.0:5000 &
nohup python manage.py celery worker &
nohup python manage.py celery beat &
nohup python manage.py celery flower --address=0.0.0.0 --port=5001 &