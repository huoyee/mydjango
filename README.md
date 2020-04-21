# mydjango
mydjango 为本人学习django使用

python3.5.0 
## 一、集成django-celery 实现异步任务

##celery 学习参考 https://www.imooc.com/video/17955

### 1.安装django-celery
`pip install django-celery`

### 2.配置django-celery
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'meizi'
]
```
### 3.创建celery所需要的数据表
`python manage.py migrate`
### 4.创建task
### 5.Worker
`python manage.py celery worker -Q queue`