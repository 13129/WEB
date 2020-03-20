from django.contrib.auth.models import AbstractUser


class Users (AbstractUser):
	'''用户'''
	class Meta:
		verbose_name = '用户'
		verbose_name_plural = verbose_name
		ordering = ['-id']

	def __str__(self):
		return self.username
