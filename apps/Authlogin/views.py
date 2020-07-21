from django.shortcuts import render,redirect,reverse#重定向
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView#内置登录视图
from django.contrib.auth import login
from django.contrib.auth import authenticate
# from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


from .models import Users
from .admin import UserCreationForm#重写User创建表单
from .forms import UserLoginForm



def login_view(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # .cleaned_data 清洗出合法数据
            data = user_login_form.cleaned_data
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个 user 对象
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request, user)
                return HttpResponseRedirect(reverse("blog:index"))
            else:
                return HttpResponse("账号或密码输入有误。请重新输入~")
        else:
            return HttpResponse("账号或密码输入不合法")

    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = { 'form': user_login_form }
        return render(request, 'login.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")



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
            login_view()
            return HttpResponseRedirect(reverse('blog:index'))
    context = {'form': form}
    return render(request,'register.html', context)


