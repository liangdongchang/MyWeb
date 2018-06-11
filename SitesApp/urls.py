'''
@author ldc

'''
from django.conf.urls import url

from SitesApp import views

app_name ='SitesApp'

urlpatterns = [
    # 首页
    url(r'^home/', views.home,name='home'),
    # 投票
    url(r'^vote/(?P<pageNum>\d+)?', views.vote,name='vote'),
    # 增加投票
    url(r'^addVote/', views.addVote, name='addVote'),
    # 打分旧地址
    url(r'^shareNav/', views.shareNav,name='shareNav'),
    # 打分首页
    url(r'^grade/', views.grade,name='grade'),
    # 增加分数
    url(r'^addGrade/', views.addGrade,name='addGrade'),
    # 知识点回顾
    url(r'^review/', views.review, name='review'),
    # 博客
    url(r'^blog/', views.blog, name='blog'),
    # 资料
    url(r'^dataBank/', views.dataBank, name='dataBank'),
    # 论坛
    url(r'^forum/', views.forum, name='forum'),
    # 我的
    url(r'^mine/', views.mine, name='mine'),
    # 登录
    url(r'^login/', views.login, name='login'),
    # 登出
    url(r'^logout/', views.logout, name='logout'),
    # 注册
    url(r'^register/', views.register, name='register'),
    # 获取验证码
    url(r'^getvcode', views.getvcode, name='getvcode'),
    # 留言
    url(r'^chat/', views.chat, name='chat'),
    # 测试
    url(r'^test/', views.test, name='test'),
    # 新增候选人
    url(r'addCandidate/',views.addCandidate,name='addCandidate')

]