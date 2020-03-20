from django.db import models
from django.utils import timezone

# Create your models here.
from apps.blog.storage import ImageStorage

#公告栏
notice_types = (('sticky', '置顶'), ('latest', '最新'), ('ordinary', '一般'))
class Notice(models.Model):
	detail = models.TextField(verbose_name="公告内容")
	level = models.CharField(max_length=30,choices=notice_types, default='最新')
	release_time = models.DateTimeField(verbose_name="发布时间", default=timezone.now)
	mod_time = models.DateTimeField(verbose_name="时间", auto_now=True)
	class Meta:
		verbose_name='网站公告'
		verbose_name_plural=verbose_name
	def __str__(self):
		return  self.detail

# 应用
class Ligthapp (models.Model):
	name = models.CharField (verbose_name = 'app', max_length = 20)
	add_time = models.DateTimeField (verbose_name = '创建时间', default = timezone.now)
	number = models.PositiveIntegerField (verbose_name = '每个应用访问数', default = 0)
	status = models.BooleanField (verbose_name = '开启/关闭', default = True)

	class Meta:
		verbose_name = '应用列表'
		verbose_name_plural = verbose_name

	def __str__ (self):  # 后台管理注册显示的类别名称
		return self.name


# 游客足迹
class Touristfp (models.Model):
	IP=models.CharField(verbose_name='ip',max_length=30,default='...')
	location=models.CharField(verbose_name='ip所在地',max_length=30,default='')
	end_point=models.CharField(verbose_name='访问端点',default='/',max_length=30)
	count=models.IntegerField(verbose_name='访问次数',default=0)

	class Meta:
		verbose_name = '访客信息'
		verbose_name_plural = verbose_name

	def __str__ (self):  # 后台管理注册显示的类别名称
		return self.IP
#网站访问总次数
class VisitNumber(models.Model):
	count=models.IntegerField(verbose_name="网站访问总次数",default=0)
	class Meta:
		verbose_name='网站访问总次数'
		verbose_name_plural=verbose_name
	def __str__(self):
		return str(self.count)
#单日访问统计
class DayNumber(models.Model):
	day=models.DateField(verbose_name="日期",default=timezone.now)
	count=models.IntegerField(verbose_name="单日访问次数",default=0)
	class Meta:
		verbose_name='单日访问次数'
		verbose_name_plural=verbose_name
	def __str__(self):
		return str(self.day)

# 友链接
class Link (models.Model):
	name = models.CharField (verbose_name = '链接名字', max_length = 20)
	linkurl = models.URLField (verbose_name = '链接网址', max_length = 100)
	linkimg = models.ImageField (verbose_name = '网站图标', storage = ImageStorage (), blank = True, null = True,
	                             upload_to = 'images/ico/%Y%m')
	add_time = models.DateTimeField (verbose_name = '添加时间', default = timezone.now)
	mod_time = models.DateTimeField (verbose_name = '修改时间', auto_now = True)

	class Meta:
		verbose_name = '友链接'
		verbose_name_plural = verbose_name

	def __str__ (self):  # 后台管理注册显示的类别名称
		return self.name
# 爬虫分析
