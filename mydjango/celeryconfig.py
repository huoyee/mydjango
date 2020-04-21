import djcelery

djcelery.setup_loader()

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