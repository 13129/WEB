from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # f分页插件
from django.shortcuts import render
from .models import *
from apps.LigthApp.models import *
from apps.LigthApp.weather import weath,cleander
from django.utils import timezone
from django.contrib.auth.decorators import login_required



# 优化重复查询语句
def global_variable (request):
	allcategory = Category.objects.values ('id','name')  # 通过Category表查出所有分类
	tui = Blog.objects.select_related('tui').filter(tui__id=1)#热门推荐
	cname = "最新文章"
	notice=Notice.objects.only('level','release_time','detail')#查询公告
	add='威海'#临时地址
	data=weath(add)
	time=timezone.now()
	cleandes=cleander()
	return locals ()


#搜索
def search (request):
	keyword = request.GET.get ("keyword")
	if not keyword:
		cname = "请输入关键字"
		return render (request, 'index.html', {'cname': cname})
	cname = keyword
	allblog = Blog.objects.defer('content').select_related('category','name').filter (title__icontains = keyword)
	page = request.GET.get ('page')  # 获取当前页面数

	paginator = Paginator (allblog, 5)  # 超过8条就分页
	try:
		allblog = paginator.page (page)  # 获取当前页码的记录
	except PageNotAnInteger:
		allblog = paginator.page (1)  # 如果用户输入的页码不是整数时,显示第1页的内容
	except EmptyPage:
		allblog = paginator.page (paginator.num_pages)

	return render (request, 'index.html', locals ())
		

# 主页
def index (request):
	banner = Banner.objects.filter (is_active = True) [0:3]  # 查询所有幻灯片数据并进行切片
	allblog = Blog.objects.defer('content').select_related('category','name').order_by ('-id')  # 首页最新推荐
	tags = Tag.objects.only('name').order_by ('?') [:8]  # 随机8个标签

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
	cname = Category.objects.get (id = cate_id)
	# 获取通过URL传进来的cid，然后筛选出对应文章
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
@login_required
def art (request, art_id):
	show = Blog.objects.select_related('category','name').prefetch_related('tagss').get (id = art_id)  # 查询指定ID的文章
	hot = Blog.objects.only('id','title').order_by ('?') [:8]  # 内容下面的您可能感兴趣的文章，随机推荐
	show.click_nums = show.click_nums + 1#阅读量
	show.save()
	return render (request, 'article.html', locals ())


# 标签
@login_required
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
