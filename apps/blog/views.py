from .models import *
from apps.LigthApp.models import *
from apps.LigthApp.weather import weath,cleander#天气日历
from apps.LigthApp.visit_info import change_info

from django.core.cache import cache
from django.utils import timezone
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # f分页插件
import pickle
import redis
import json
import datetime
from django_redis import get_redis_connection





class 

# 优化重复查询语句
def global_variable (request):
	allcategory = Category.objects.values ('id','name')  # 通过Category表查出所有分类
	banner = Banner.objects.filter(is_active = True)[0:3] # 查询所有幻灯片数据并进行切片
	tui = Blog.objects.select_related('tui').filter(tui__id=1).order_by('-click_nums')[:10]#热门推荐

	cname = "最新文章"
	notice=Notice.objects.only('level','release_time','detail')#查询公告

	add='莱西'#临时地址
	data=weath(add)
	time=timezone.now()
	cleandes=cleander()

	return locals ()


'''搜索'''
def search (request):
	keyword = request.GET.get ("search")
	tags_name = request.GET.get('tag')
	#表单为空时
	if not keyword:
		cname = "请输入关键字"
		return render (request, 'index.html', {'cname': cname})
	else:
		cname = '关键词：'+keyword
		allblog = Blog.objects.defer('content').select_related('category','name').prefetch_related('tagss').\
			filter (title__icontains = keyword)
		#搜索所属文章的标签结果
		al_tags=[ al.tagss.all() for al in allblog ]
		tags=set([ t1  for t in al_tags for t1 in t ])#标签去重
	#标签请求时筛选文章
		if tags_name:
			cname='关键词：'+keyword+'  标签：'+tags_name
			allblog=allblog.filter(tagss__name = tags_name)
	page = request.GET.get ('page')  # 获取当前页面数
	paginator = Paginator (allblog, 5)  # 超过8条就分页
	try:
		allblog = paginator.page (page)  # 获取当前页码的记录
	except PageNotAnInteger:
		allblog = paginator.page (1)  # 如果用户输入的页码不是整数时,显示第1页的内容
	except EmptyPage:
		allblog = paginator.page (paginator.num_pages)
	return render (request, 'index.html', locals ())


'''主页'''
def index (request):
	change_info(request)
	tags_name = request.GET.get('tag')
	if  tags_name:
		# 点击标签筛选对应文章，并随别的标签
		cname = '标签：' + tags_name
		allblog = Blog.objects.defer('content').select_related('category', 'name') \
			.prefetch_related('tagss').filter(tagss__name = tags_name)  # 多对多查询
	else :
		allblog = Blog.objects.defer('content').select_related('category', 'name')  # 首页最新推荐
	tags = Tag.objects.only('name').order_by('?')[:8]

	page = request.GET.get ('page')  # 获取当前页面数
	paginator = Paginator (allblog, 5)  # 超过8条就分页
	try:
		allblog = paginator.page (page)  # 获取当前页码的记录
	except PageNotAnInteger:
		allblog = paginator.page (1)  # 如果用户输入的页码不是整数时,显示第1页的内容
	except EmptyPage:
		allblog = paginator.page (paginator.num_pages)
	return render (request, 'index.html', locals ())  # 所有变量值传到index.html页面


#查询列表
def cate (request, cate_id):
	cname = Category.objects.get (id = cate_id)# 获取通过URL传进来的cid，然后筛选出对应文章
	allblog = Blog.objects.defer('content').select_related('category','name').filter (category__id = cate_id)
	page = request.GET.get ('page')  # 获取当前页面数
	paginator = Paginator (allblog, 5)  # 超过5条就分页
	try:
		allblog = paginator.page (page)  # 获取当前页码的记录
	except PageNotAnInteger:
		allblog = paginator.page (1)  # 如果用户输入的页码不是整数时,显示第1页的内容
	except EmptyPage:
		allblog = paginator.page (paginator.num_pages)
	# 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
	return render (request, "category.html", locals ())


# 内容
def art (request, art_id):
	#连接redis 数据库
	conn = get_redis_connection()

	show = Blog.objects.select_related('category','name').prefetch_related('tagss').get (id = art_id)  # 查询指定ID的文章
	click_nums = click_num(request,conn,art_id,show)#返回点击数
	hot = Blog.objects.only('id','title').order_by ('?') [:8]  # 内容下面的您可能感兴趣的文章，随机推荐
	# show.increated_nums()#自定义模型方法


	return render (request, 'article.html', locals ())


#redis blog_info博客信息表
def click_num(request,conns,art_id,shows):
	UserName = request.user.username	#当前登录用户
	nowtime = str(datetime.datetime.now())#获取当前时间
	#判断散列表中是否有 key
	#判断有key时，更新value
	#文章访问足迹
	str_inof = UserName+':?:'+nowtime

	if conns.hexists('blog_info',art_id):
		info = conns.hget('blog_info',art_id)
		info = json.loads(str(info,'utf-8'))
		if not (info['views'] % 100):
			shows.increated_nums(info['views'])
			info['blog_history'] = []	#初始化足迹
		
		info['views'] += 1	#获取点击量
		info['blog_history'].append(str_inof)	#获取足迹信息列表并更新

		conns.hset('blog_info',art_id,json.dumps({'views':info['views'],'blog_history':info['blog_history']}))
		return info['views']	
	else:
		userinfo = [str_inof]
		conns.hset("blog_info", art_id, json.dumps({'views':shows.click_nums,'blog_history':userinfo}))


# 标签
def tag (request):
	tags = Tag.objects.all()
	tags_list = list (tags)  # 列表化QuertySet对象
	one_tag=dict(zip([tl for tl in tags_list ],
		[Blog.objects.filter (tagss__id = tl.id).values("tagss").count() for tl in tags_list]))
	#转化为字典{<Tag: name>: 2, <Tag: name>: 0}//未使用.items方法
	all_tags = sorted (one_tag.items (), key = lambda d: d [1], reverse = True)  # 根据标签数量大>小排序
	return render (request, "tags.html", locals ())



def fzf (request):
	return render (request, '404.html')
