"""MySites URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url,include
from django.contrib import admin


from SitesApp import views
from SitesApp.admin import mysite

urlpatterns = [
    url('admin/', mysite.urls),
	# 首页
    url('^$', views.index),
	url('^home/', views.index),
	# 打分旧地址
	url('^vote/shareNav/',views.shareNav),
	url('^app/',include('SitesApp.urls',namespace='sitesApp'))

]
