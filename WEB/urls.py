"""WEB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include
from django.urls import path, re_path

urlpatterns = [
	re_path (r'^admin/', admin.site.urls),
	re_path (r'',include('apps.blog.urls',namespace='blog')),
	re_path (r'^auth/', include ('apps.Authlogin.urls',namespace='Authlogin')),
	re_path (r'^app/', include ('apps.LigthApp.urls',namespace='LigthApp')),
]

from django.conf import settings
if settings.DEBUG:
	from django.conf.urls.static import static
	import debug_toolbar

	urlpatterns += static (
		settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

	urlpatterns = [path('__debug__/', include(debug_toolbar.urls)),] + urlpatterns