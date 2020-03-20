'''
Created on 2020年3月4日
应用apps
插件
api开发
@author: x1312
'''
from django.urls import re_path,path
from apps.LigthApp.views import sumall

app_name = 'LigthApp'
urlpatterns = [
	re_path (r'^sumall/', sumall, name = 'sumall'),
]
