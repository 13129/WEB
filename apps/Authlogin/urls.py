'''
Created on 2019年11月20日
登录界面---templates
@author: x1312
'''

from django.urls import path,re_path,include
from django.contrib.auth.views import LoginView,LogoutView
from.views import register



app_name='Authlogin'
urlpatterns = [
    re_path(r"^login/$",LoginView.as_view(template_name='login.html'),name='login'),
    re_path(r"^logout/$",LogoutView.as_view(template_name='index.html'),name='logout'),
    re_path(r"^register/$",register,name='register'),
    #re_path()

]
