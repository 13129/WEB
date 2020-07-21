from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,render,redirect,reverse,render_to_response
from django.shortcuts import HttpResponseRedirect

from django.contrib.auth import authenticate,get_user

from django.conf import settings
from django.core.cache import cache
from .models import Users



class AuthMiddleWare(MiddlewareMixin):
    '''
    登录权限控制
    未登录不能进行任何操作
    '''
    url_path=['/auth/login/','/auth/logout/','admin/login/?next=/admin/','/auth/register/']
    
    def process_request(self,request):
        if request.path =='/auth/logout/':
            if  request.user.is_authenticated:
                response = HttpResponseRedirect(reverse('Authlogin:login'))  #重定向
                #判断sessionId是否已经清除
                try:
                    response.delete_cookie('sessionId') #s删除cookie
                    request.session.flush()  #清除session
                except Exception as err:
                    return response         
                return response

        if not (request.path in self.url_path):
            if  not request.user.is_authenticated:
                return HttpResponseRedirect(reverse('Authlogin:login'))

    def process_response(self,request,response):
        
        return response