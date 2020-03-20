from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin#从django继承过来定制
from django.contrib.auth.forms import ReadOnlyPasswordHashField#哈希加密
from .models import Users
from django.utils.translation import ugettext_lazy as _#字段国际化

class UserCreationForm(forms.ModelForm):
	"""创建新用户的表单"""
	username  = forms.CharField(label = '用户名',widget = forms.TextInput)
	password1 = forms.CharField(label = '密码', widget = forms.PasswordInput)
	password2 = forms.CharField(label = '确认密码', widget = forms.PasswordInput)
	email     = forms.EmailField(label = '邮箱',widget = forms.EmailInput)

	class Meta:
		model = Users
		fields = ['username','password1','password2','email']

	def clean_password2(self):
		# 检查密码是否匹配
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("密码不匹配")
		return password2

	def save(self, commit = True):
		# 密码哈希加密
		user = super(UserCreationForm, self).save(commit = False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user


class UserChangeForm(forms.ModelForm):
	"""用于修改用户的表单。将密码字段替换为管理员的密码加密显示字段。"""
	password = ReadOnlyPasswordHashField()#hash加密

	class Meta:
		model = Users
		fields=['username','password','email']
	def clean_password(self):
		# 无论用户提供什么，都返回初始值,字段无权访问初始值
		return self.initial["password"]


class AuthloginAdmin(UserAdmin):
	def __init__(self, *args, **kwargs):
		super(AuthloginAdmin, self).__init__(*args, **kwargs)
		self.list_display = ('username',  'email', 'is_active', 'is_staff', 'is_superuser')
		self.search_fields = ('username', 'email',)
		self.list_filter = ('last_login',)
		self.form = UserChangeForm  # 编辑用户表单，使用自定义的表单
		self.add_form = UserCreationForm
	#重写用户权限
	def changelist_view(self, request, extra_context = None):
	# 这个方法在源码的admin/options.py文件的ModelAdmin这个类中定义，不同权限的用户，返回的表单内容不同
		if not request.user.is_superuser:# 用于显示用户模型的字段。这些将覆盖基本UserAdmin上的定义,引用auth.User上的特定字段。
			self.fieldsets = ((None,
			                   {'fields': ('username', 'password',)}),
			                  (_('Personal info'), {'fields': ('email',)}),  # _ 将('')里的内容国际化,这样可以让admin里的文字自动随着LANGUAGE_CODE切换中英文
			                  (_('Permissions'), {'fields': ('is_active', 'is_staff', 'groups')}),
			                  (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
			                  )
			# 这里('Permissions')中没有'is_superuser',此字段定义UserChangeForm表单中的具体显示内容，并可以分类显示
			self.add_fieldsets = ((None, {'classes': ('wide',),
			                              'fields': ('username', 'password1', 'password2', 'email', 'is_active',
			                                         'is_staff', 'groups'),
			                              }),
			)
		else:  # super账户可以做任何事
			self.fieldsets = ((None, {'fields': ('username', 'password',)}),
	                  (_('Personal info'), {'fields': ('email',)}),
	                  (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
	                  (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
	        )
			self.add_fieldsets = ((None, {'classes': ('wide',),
	                              'fields': ('username', 'password1', 'password2', 'email', 'is_active',
	                                         'is_staff', 'is_superuser', 'groups'),
	                              }),
			)
		return super(AuthloginAdmin, self).changelist_view(request, extra_context)



# 注册新的UserAdmin ...
admin.site.register(Users, AuthloginAdmin)
#由于我们没有使用Django的内置权限，
#从admin注销组模型。
#admin.site.unregister(Group)

