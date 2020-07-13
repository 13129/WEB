import os
from .storage import ImageStorage
from django.conf import settings
from django.db import models
from django.utils import timezone



from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
"""数据库表"""


# 分类
class Category (models.Model):
	name = models.CharField (verbose_name = '文章类别', max_length = 20)
	class Meta:
		verbose_name = '文章类别'
		verbose_name_plural = verbose_name
	def __str__ (self):
		return self.name

# 推荐位
class Tui (models.Model):
	name = models.CharField ('推荐位', max_length = 100)
	class Meta:
		verbose_name = '推荐位'
		verbose_name_plural = verbose_name
	def __str__ (self):
		return self.name


# 轮播图
class Banner (models.Model):
	text_info = models.CharField ('标题', max_length = 50, default = '')
	img = ProcessedImageField (verbose_name = '轮播图',
	                           upload_to = 'images/banner/%Y%m',
	                           storage = ImageStorage (),
	                           processors = [ResizeToFill (820, 200)],
	                           format = 'jpeg',
	                           options = {'quality': 72},
	                           null = True,
	                           blank = True, )

	link_url = models.URLField ('图片链接', max_length = 1000)
	is_active = models.BooleanField ('是否是active', default = False)
	class Meta:
		verbose_name = '轮播图'
		verbose_name_plural = '轮播图'
	def __str__ (self):
		return self.text_info


# 文章标签
class Tag (models.Model):
	name = models.CharField (verbose_name = '文章标签', max_length = 20)
	class Meta:
		verbose_name = '文章标签'
		verbose_name_plural = verbose_name
	def __str__ (self):
		return self.name


from ckeditor.fields import RichTextField
# 博客
class Blog (models.Model):
	name = models.ForeignKey (settings.AUTH_USER_MODEL, verbose_name ='作者', on_delete = models.CASCADE)
	title = models.CharField (verbose_name = '标题', max_length = 100)
	content=RichTextField(verbose_name = '正文',config_name = 'my_config')
	tui = models.ForeignKey (Tui, on_delete = models.DO_NOTHING, verbose_name = '推荐位', blank = True, null = True)
	create_time = models.DateTimeField (verbose_name = '创建时间', default = timezone.now)
	modify_time = models.DateTimeField (verbose_name = '修改时间', auto_now = True)
	click_nums = models.IntegerField(verbose_name = '点击量', default = 0)
	category = models.ForeignKey (Category, verbose_name = '文章类别', on_delete = models.DO_NOTHING)
	tagss = models.ManyToManyField (Tag, verbose_name = '文章标签', )  # 多对多的外键关系
	img = models.ImageField (upload_to = 'images/blog/%Y%m', storage = ImageStorage (), verbose_name = '封面图片', blank = True,
	                         null = True)

	'''使用图片上传需要模块pillow,default=timezone.now和auto_now_add只能使用一个
	使用另一个apps的模型表需要[apps名称].[模型表名称]使用单引号包括其中
	'''

	class Meta:
		verbose_name = '我的博客'
		verbose_name_plural = verbose_name
		ordering = ['-modify_time']

	def increated_nums(self):#增加模型方法，缺陷：高访问下会造成数据不准
		self.click_nums+=1
		self.save(update_fields = ['click_nums',])

	def tagss_list(self):
		return ','.join([i.name for i in self.tagss.all()])

	def __str__ (self):
		return self.title





