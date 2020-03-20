'''
Created on 2019年11月20日

@author: Administrator
'''
from django.urls import path, re_path,include
from apps.blog import views
from apps.blog.views import *

app_name = 'blog'
urlpatterns = [
	re_path (r"^$", index, name = "index"),  # 主页

	re_path (r"^art/$", views.art, name='art'),
	re_path (r"^art/(?P<art_id>\d+)/$", art, name = "art"),  # 内容页

	re_path (r'cate/$',cate,name='cate'),
	re_path (r"^cate/(?P<cate_id>\d+)/$", cate, name = "cate"),  # 列表

	re_path (r"^tag/$",tag,name="tag"),#标签云
	re_path (r"^search/$", views.search, name ="search"),
	re_path (r"^404/$", fzf, name = "fzf"),  # 自定义404
]
