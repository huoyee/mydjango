from django.http import JsonResponse
from django.shortcuts import render
from django import views
import requests

import os

# Create your views here.

#执行爬虫
class Run(views.View):
    def post(self,request):
        return JsonResponse('执行爬虫')
    def get(self,request):
        return render(request,'static/meizi/index.html')