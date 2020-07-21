"""
Django settings for WEB project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys
from django.views.static import serve

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname (os.path.dirname (os.path.abspath (__file__)))
sys.path.insert (0,BASE_DIR)
sys.path.insert (0, os.path.join (BASE_DIR, 'apps'))
sys.path.insert (0, os.path.join (BASE_DIR, 'extra_apps'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/
# 图片的路径
MEDIA_ROOT = os.path.join (BASE_DIR, 'media')  # 图片存取的绝对路径
MEDIA_URL = '/media/'  # 图片存取的相对路径
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*)7#@_pyqq7wzvdd@9^^**w4@iud356jndp(%ox(37-wdp)%)j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # 生产环境开启

ALLOWED_HOSTS = ['10.0.0.25','127.0.0.1']


# Application definition
#Django应用
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'blog',
	'Authlogin',
	'LigthApp',
	'djcelery',
	'debug_toolbar',
	'ckeditor',
	'imagekit',
	'rest_framework',
	'apps.blog.templatetags',
]

#中间件
MIDDLEWARE = [
	'debug_toolbar.middleware.DebugToolbarMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	# 'apps.LigthApp.mymidleware.Accessfrequency',
	'apps.Authlogin.midleware.AuthMiddleWare',
]

#根url开始文件
ROOT_URLCONF = 'WEB.urls'

#配置视图模板
TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join (BASE_DIR, 'templates')],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
				'apps.blog.views.global_variable',  # blog.views中定义的全局函数
			],
		},
	},
]

WSGI_APPLICATION = 'WEB.wsgi.application'

# Database MYSQL
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'web',  # 你的数据库名称
		'USER': 'root',  # 你的数据库用户名
		'PASSWORD': '123456',  # 你的数据库密码
		'HOST': '127.0.0.1',  # 你的数据库主机，留空默认为localhost
		'PORT': '3306',  # 你的数据库端口
		'TEST':{
			'CHARSET':'utf8mb4',
			'COLLATION':'utf8mb4_bin',
		}
	}
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]
# settings.py
...
# ckeditor配置
CKEDITOR_CONFIGS = {
    # 将这份配置命名为 my_config
    'my_config': {
        'skin': 'moono-lisa',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_Full': [
            ['Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike', 'SpellChecker', 'Undo', 'Redo'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule'],
            ['TextColor', 'BGColor'],
            ['Smiley', 'SpecialChar'],
            # 在工具栏中添加该功能的按钮
            ['CodeSnippet'], ['Source'],

        ],
        'toolbar': 'Full',
        'height': 291,
        'width': 835,
        'filebrowserWindowWidth': 940,
        'filebrowserWindowHeight': 725,
        # 添加的插件
        'extraPlugins': 'codesnippet',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
	os.path.join (BASE_DIR, 'static'),
]
# STATIC_ROOT = os.path.join(BASE_DIR, "static")

AUTH_USER_MODEL ='Authlogin.Users'

#登录url
LOGIN_URL = '/auth/login/'

# 自定义登录认证配置，声明重写方法
# AUTHENTICATION_BACKENDS=['Authlogin.views.CustomModelBackend', ]
import djcelery
#celery配置
djcelery.setup_loader()
# celery中间人 redis://redis服务器所在的ip地址:地址/数据库号
BROKER_URL = 'redis://127.0.0.1:6379/0'
# celery结果返回，可用于跟踪结果
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
# celery内容等消息的格式设置
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
# celery时区设置，使用TIME_ZONE
CELERY_TIMEZONE = TIME_ZONE


# cache 开发调试缓存配置-
# CACHES={
# 	'default':{
# 		'BACKEND':'django.core.cache.backends.dummy.DummyCache',    #缓存引擎
# 		'TIMEOUT':300,              #缓存超时时间 None表示永不过期，0表示立即过期，默认300秒
# 		'OPTIONS':{
# 			'MAX_ENTRIES':300,      #最大缓存记录的数量（默认300）
# 			'CULL_FREQUENCY':3,     # 缓存到达最大个数之后，剔除缓存个数的比例，即：1/CULL_FREQUENCY（默认3）
# 		},
# 	}
# }
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "CONNECTION_POOL_KWARGS": {"max_connections": 100},
			"PASSWORD":"12345"
        }
    }
}
#session保存在缓存中
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# SESSION_COOKIE_AGE =80000 # 默认两周单位秒
SESSION_COOKIE_HTTPONLY = True # 设置session cookie是httponly
SESSION_COOKIE_NAME = 'sessionId' # session cookie的名字
SESSION_COOKIE_PATH = '/' # session cookie的path
SESSION_COOKIE_SECURE = False # session cookie的secure
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


INTERNAL_IPS=['127.0.0.1',]#debug_toolbar配置。。。中间件
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

