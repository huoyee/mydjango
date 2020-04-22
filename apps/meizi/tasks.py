
#

from celery.task import Task

class Testcelery(Task):
    name = 'testcelery'
    def run(self,*args,**kwargs):
        a = 1+1
        print(a)