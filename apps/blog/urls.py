'''
Created on 2019年11月20日

@author: Administrator
'''
from django.views.decorators.cache import cache_page#缓存设置时间的意义在于，多长时间内的内容不变
from django.urls import path, re_path,include
from apps.blog.views import *

app_name = 'blog'
urlpatterns = [
	re_path (r'^$', cache_page(60*15)(index), name = 'index'),  # 主页

	re_path (r'^art/$', cache_page(60*15)(art), name='art'),
	re_path (r'^art/(?P<art_id>\d+)/$', cache_page(60*15)(art), name = 'art'),  # 内容页

	re_path (r'cate/$',cache_page(60*15)(cate),name='cate'),
	re_path (r'^cate/(?P<cate_id>\d+)/$', cache_page(60*15)(cate), name = 'cate'),  # 列表

	re_path (r'^tag/$',tag,name="tag"),#标签云
	re_path (r'^search/$',search, name ="search"),
	re_path (r'^search/search=(?P<search>\w+)&tag=(?P<tag>\w+)',search,name="search"),#搜索+标签过滤
	re_path (r'^404/$', fzf, name = 'fzf'),  # 自定义404
]
