"""campusRecruitmentOS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from django.views import static ##新增
from django.conf import settings ##新增
from django.conf.urls import url ##新增
from user.views import index, captcha_img
# 主路由设置
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('index', index),
    path('user/', include(('user.urls', 'user'))),  # 用户系统
    path('company/', include(('company.urls', 'company'))),  # 企业系统
    path('captcha_img/', captcha_img, name='captcha_img'),
    #静态文件夹路由
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),
]
