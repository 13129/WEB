import os
from .models import Blog,Banner
from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save,pre_delete,post_init
from django.core.cache  import cache
'''
信号文件夹
'''

CACHE_TIMEOUT_2D=60*15


#缓存信号
# @receiver(post_init,sender=Blog,dispatch_uid='model_blog_save_active')
# def my_blog_active(instance,**kwargs):
# 	instance.__original_modify_time=instance.modify_time

# @receiver(post_save,sender=Blog,dispatch_uid='model_blog_save_active')
# def my_blog_active2(instance,created,**kwargs):
# 	print("信号来了")
# 	#如果有修改时重置文章缓存
# 	allblog = Blog.objects.get(id=instance.id)
# 	cache.get("allblog_%s",instance.id,allblog,CACHE_TIMEOUT_2D)
#
# 	#如果有新建博客就重置首页缓存
# 	if created:
# 		allblog=Blog.objects.defer('content').select_related('category','name')
# 		print("新建",allblog)
# 		cache.set("allblog_top",allblog,CACHE_TIMEOUT_2D)




#更改图片删除前一个·图片信号
@receiver (pre_save, sender = Blog, dispatch_uid = "model_Blog_save_img")
def my_blogimg (sender, instance, **kwargs):

	if not instance.id:
		return False
	try:
		old_file = Blog.objects.get (id = instance.id).img
	except Blog.DoesNotExist:
		return False

	new_file = instance.img
	if not old_file == new_file:
		if os.path.isfile (old_file.path):
			os.remove (old_file.path)



@receiver (pre_save, sender = Banner, dispatch_uid = "Model_Banner_img")
def my_bannerimg (sender, instance, **kwargs):
	# instance.img.delete(False)
	if not instance.id:
		return False
	try:
		old_file = Banner.objects.get (id = instance.id).img
	except Banner.DoesNotExist:
		return False
	new_file = instance.img
	if not old_file == new_file:
		if os.path.isfile (old_file.path):
			os.remove (old_file.path)
