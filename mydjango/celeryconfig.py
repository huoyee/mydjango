from datetime import timedelta
from celery import platforms
import djcelery

from celery.schedules import crontab
#celery不能用root用户启动问题 C_FORCE_ROOT environment
platforms.C_FORCE_ROOT = True  #加上这一行
djcelery.setup_loader()

BROKER_BACKEND = 'redis'
BROKER_URL = 'redis://localhost:6379/1'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'

CELERY_QUEUES = {
    'beat_tasks':{
        'exchange':'beat_tasks',
        'exchange_type':'direct',
        'binding_key' : 'beat_tasks'
    },
    'work_queue':{
        'exchange':'work_queue',
        'exchange_type':'direct',
        'binding_key':'work_queue'
    }
}

#默认
CELERY_DEFAULT_QUEUE = 'work_queue'

CELERY_IMPORTS=(
    'apps.meizi.tasks'
)

#有些情况可以防止死锁
CELERYD_FORCE_EXECV = True

#设置并发的worker数量
CELERYD_CONCURRENCY = 4

#运行重试
#CELERY_ACKS_LATE = True

#每个worker 最多执行100个任务被销毁，可以防止内存泄漏
CELERYD_MAX_TASKS_PER_CHILD = 100

#单个任务最大运行时间
#CELERYD_TASK_TIME_LIMIT = 12*30

CELERYBEAT_SCHEDULE = {
    'task1':{
        'task': 'testcelery',
        #'schedule': crontab(minute='*/6') ,#10秒执行一次
        'schedule':timedelta(seconds=5),
        'options':{
            'queue':'beat_tasks'
        }
    }
}