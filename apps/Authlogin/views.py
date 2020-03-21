from django.shortcuts import render,redirect,reverse#重定向
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView#内置登录视图
from django.contrib.auth import authenticate
from .admin import UserCreationForm#重写User表单


def register(request):
    """注册新用户"""
    if request.method!='POST':
    #显示空的注册表单
        form = UserCreationForm()
    else:
        # 处理填写好的表单
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # 让用户自动登录，再重定向到主页
            user = authenticate(username=new_user.username,password=request.POST['password1'])
            LoginView.as_view()
            return HttpResponseRedirect(reverse('blog:index'))
    context = {'form': form}
    return render(request,'register.html', context)

