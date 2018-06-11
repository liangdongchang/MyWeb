from django.contrib import admin

# Register your models here.
#注册用户表、投票类型、候选者表、聊天记录、知识点回顾表、博客类型、博客信息表、资料信息表


from SitesApp.models import *

# 自定义站点管理
class MySite(admin.AdminSite):
	site_title = '个人网站'
	site_header = '我的站点数据管理'
	site_url = '/'

mysite = MySite()

# 用户的后台管理
class UserAdmin(admin.ModelAdmin):
	# 检索字段
	search_fields = ['uName','uIP',]
	# 要显示的字段
	list_display = ['id','uName','uIP' ,'uEmail' ,'uNickName' ,'uGender','uAge' ,'uIcon' ,'isDelete']
	# 分组过滤的字段
	list_filter = ['uName','uNickName','uGender','uAge','isDelete']

# 投票类型的后台管理
class VoteTypeAdmin(admin.ModelAdmin):
	# 检索字段
	search_fields = ['vType','isDelete']
	# 要显示的字段
	list_display = ['id','vType','vInfo','isDelete',]
	# 分组过滤的字段
	list_filter = ['vType','isDelete',]


# 候选者的后台管理
class CandidateAdmin(admin.ModelAdmin):
	# 检索字段
	search_fields = ['cName','cAge','cTimes','cVotes','cPinyin','isDelete',]
	# 要显示的字段
	list_display = ['id','cName','cAge','cEmail','cDeclaration','cIcon','cTimes','cVotes','cPinyin','isDelete',]
	# 分组过滤的字段
	list_filter = ['cName','cAge','cTimes','cVotes','cPinyin','isDelete',]


# 投票记录的后台管理
class VoteRecordAdmin(admin.ModelAdmin):
	# 检索字段
	search_fields = ['vUserId','vDate','vCandidateId','vComIP','vTypeId','vPolls','vTimes','isDelete']
	# 要显示的字段
	list_display = ['id','vUserId','vDate','vCandidateId','vComIP','vTypeId','vPolls','vTimes','isDelete']
	# 分组过滤的字段
	list_filter = ['vUserId','vDate','vCandidateId','vComIP','vTypeId','vPolls','vTimes','isDelete']

# 聊天记录的后台管理
class ChatRecordAdmin(admin.ModelAdmin):
	# 检索字段
	search_fields = ['crUserId','crNickName','crIP','crDateTime','crInfo','crTopic','crType','isDelete']
	# 要显示的字段
	list_display = ['id','crUserId','crNickName','crIP','crDateTime','crInfo','crTopic','crType','isDelete']
	# 分组过滤的字段
	list_filter = ['crUserId','crNickName','crIP','crDateTime','crInfo','crTopic','crType','isDelete']

mysite.register(User,UserAdmin)
mysite.register(VoteType,VoteTypeAdmin)
mysite.register(Candidate,CandidateAdmin)
mysite.register(VoteRecord,VoteRecordAdmin)
mysite.register(ChatRecord,ChatRecordAdmin)
mysite.register(Review)
mysite.register(BlogType)
mysite.register(Blogs)
mysite.register(DataBank)