# mydjango
mydjango 为本人学习django使用

## 一、集成django-celery 
实现异步任务和定时任务  
### 包版本
```python
Django==2.1
celery==3.1.25
django-celery==3.3.1
django-redis==4.11.0
redis==2.10.6
```
###django-celery 参考 
[慕课网视频](https://www.imooc.com/video/17955)

### 1.安装django-celery
`pip install django-celery`

### 2.添加djcelery模块
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery'
]
```
### 3.配置celery
项目目录下创建celeryconfig.py文件
```python
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

```
### 3.创建celery所需要的数据表
`python manage.py migrate`
### 4.创建task
app 目录创建tasks.py 

### 5.定时任务
|Example|Meaning|
|---|---|
|crontab()|每分钟执行|
|crontab(minute=0, hour=0)|每天凌晨执行|
|crontab(minute=0, hour=’*/3’)|每三个小时执行: midnight, 3am, 6am, 9am, noon, 3pm, 6pm, 9pm. |
|crontab(minute=0,hour=’0,3,6,9,12,15,18,21’)|同上|
|crontab(minute=’*/15’)|每十五分钟执行 |
|crontab(day_of_week=’sunday’)|星期天每分钟执行 |
|crontab(minute=’‘,hour=’‘, day_of_week=’sun’)|同上|
|crontab(minute=’*/10’,hour=’3,17,22’, day_of_week=’thu,fri’)|每十分钟执行, 但是只在星期四、五的 3-4 am, 5-6 pm, and 10-11 pm|
|crontab(minute=0, hour=’/2,/3’)|每两个小时及每三个小时执行，意思是: 除了下面时间的每个小时: 1am, 5am, 7am, 11am, 1pm, 5pm, 7pm, 11pm|
|crontab(minute=0, hour=’*/5’)|每五个小时执行。这意味着将在 3pm 而不是 5pm 执行 (因为 3pm 等于 24 小时制的 15, 能被 5 整除)|
|crontab(minute=0, hour=’*/3,8-17’)|每三个小时, 以及 (8am-5pm)| 之间的小时执行|
|crontab(0, 0, day_of_month=’2’)|每个月的第二天执行 |
|crontab(0, 0, day_of_month=’2-30/3’)|每个月的偶数天执行|
|crontab(0, 0,day_of_month=’1-7,15-21’)|每个月的第一个和第三个星期执行|
|crontab(0, 0, day_of_month=’11’,month_of_year=’5’)|每年五月份的第十一天执行|
|crontab(0, 0,month_of_year=’*/3’)|每个季度的第一个月执行|
### 5.运行
####启动服务
`python manage.py runserver 0.0.0.0:8000`
####启动worker  
`python manage.py celery worker -l info`
####启动beat  
`python manage.py celery beat -l info`
####启动flower
`python manage.py celery flower --basic-auth=name:pwd`