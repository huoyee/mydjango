
#

from celery.task import Task

class Testcelery(Task):
    def run(self):
        a = 1+1
        print(a)