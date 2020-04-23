from django.http import JsonResponse
from django.shortcuts import render
from django import views
import requests

import os

from apps.meizi.tasks import Testcelery
# Create your views here.

#执行爬虫
class Run(views.View):
    def post(self,request):
        return JsonResponse('执行爬虫')
    def get(self,request):
        return render(request,'static/meizi/index.html')

class downfile(views.View):

    def get(self,request):
        #Testcelery.delay()
        Testcelery.apply_async(args=('hello',),kwargs={'aa':'bb'}, queue='work_queue')
        return JsonResponse({"result":'ok'})

class MeiziDown(views.View):

    def get(self,request):

        pass
