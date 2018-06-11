from django.db import models
#
# # Create your models here.
# # 自定义管理表类
from django.db.models import Manager
#
#
#
# # 给表设置Manager类型的属性,名称任意
# # 设置以后,框架将不在为表生成隐式属性objects
# # 定义管理器对象的目的,在于: 1、修改框架的默认查询设置 2、为表增加新的自定义功能
#
class MyManager(Manager):
	# 查询所有记录时默认不包含被逻辑删除的记录
	def get_queryset(self):
		return super().get_queryset().exclude(isDelete=True)

# # 用户表
class User(models.Model):
	'''用户名、密码、电脑IP、邮箱、昵称、性别、年龄、头像、token、注册时间'''
	uName = models.CharField(max_length=20,unique=True,verbose_name='用户名')
	uPwd = models.CharField(max_length=32, default=None, null=True,verbose_name='密码')
	uIP = models.CharField(max_length=20,default=None, null=True,verbose_name='电脑IP')
	uEmail = models.CharField(max_length=20, default=None, null=True,blank=True,verbose_name='邮箱')
	uNickName = models.CharField(max_length=20, default='guest', null=True,verbose_name='昵称')
	uGender = models.NullBooleanField(default=None,null=True,verbose_name='性别')
	uAge = models.IntegerField(default=0,verbose_name='年龄')
	uIcon = models.ImageField(default=None,null=True,blank=True,verbose_name='头像')
	uToken = models.CharField(max_length=64, default=None, null=True, blank=True, unique=True,verbose_name='登录状态')
	uDateTime = models.DateTimeField(auto_now=True,verbose_name='时间')
	isDelete = models.BooleanField(default=False,verbose_name='是否删除')
	# 使用自定义的管理表类
	uManager = MyManager()
	def __str__(self):
		return self.uName

	class Meta:
		# 自定义表名
		db_table = 'users'

# 投票类型表（投票、打分）
class VoteType(models.Model):
	'''类型、简介'''
	vType = models.CharField(max_length=20, unique=True,verbose_name='类型')
	vInfo = models.CharField(max_length=200,verbose_name='简介')
	isDelete = models.BooleanField(default=False,verbose_name='是否删除')

	# 使用自定义的管理表类
	vManager = MyManager()

	def __str__(self):
		return self.vType

	class Meta:
		# 自定义表名
		db_table = 'voteType'

#候选者表
class Candidate(models.Model):
	'''姓名、年龄、邮箱、竞选宣言、头像、竞选轮数、票数、拼音首字母'''
	cName = models.CharField(max_length=20,unique=True,verbose_name='姓名')
	cAge = models.IntegerField(default=0,verbose_name='年龄')
	cEmail = models.CharField(max_length=20, default=None, null=True,blank=True,verbose_name='邮箱')
	cDeclaration = models.CharField(max_length=300,default='我就是我，不一样的烟火',verbose_name='口号')
	cIcon = models.ImageField(default='think.jpg', null=True, blank=True,verbose_name='头像')
	cTimes = models.IntegerField(default=1,verbose_name='轮数')
	cVotes = models.IntegerField(default=0,verbose_name='票数')
	cPinyin = models.CharField(max_length=20,default='',verbose_name='拼音码')
	isDelete = models.BooleanField(default=False,verbose_name='是否删除')

	# 外键 候选者表与投票类型是一对多的关系一个投票类型对应多个候选者
	cVoteType = models.ForeignKey(VoteType,on_delete=models.SET_NULL,blank=True,null=True)

	cManager = MyManager()

	def __str__(self):
		return self.cName

	class Meta:
		# 自定义表名
		db_table = 'candidates'
		# 按票数进行排序，降序
		ordering= ['-cVotes',]

# 用户投票记录表
class VoteRecord(models.Model):
	'''用户名、时间、投票对象、电脑IP、投票类型、票数（分数）、投票轮数'''
	# 投票记录表与用户表是一对一的关系
	vUserId = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,verbose_name='用户名')
	vDate = models.DateField(auto_now=True,verbose_name='时间')
	# 投票记录表与候选者表是一对多的关系
	vCandidateId = models.ForeignKey(Candidate, on_delete=models.SET_NULL, blank=True, null=True,verbose_name='投给谁')
	vComIP = models.CharField(max_length=20,default=None, null=True,verbose_name='电脑IP')
	# 投票记录表与投票类型表是一对多的关系
	vTypeId = models.ForeignKey(VoteType, on_delete=models.SET_NULL, blank=True, null=True,verbose_name='投票类型')
	# 票数
	vPolls = models.IntegerField(default=0,verbose_name='票数')
	# 投票轮数
	vTimes = models.IntegerField(default=1,verbose_name='轮数')
	isDelete = models.BooleanField(default=False,verbose_name='是否删除')


	# 获取用户信息
	def getUser(self):
		return self.vUserId

	def getCandidate(self):
		return self.vCandidateId

	def getType(self):
		return self.vTypeId

	class Meta:
		db_table = 'voteRecords'

# 聊天记录表
class ChatRecord(models.Model):
	'''发言人名称、电脑ip、时间、内容、话题、类型'''
	# 聊天记录表与用户表是一对一的关系
	crUserId = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True,verbose_name='发言人')
	crNickName = models.CharField(max_length=20,default='guest',verbose_name='昵称')
	crIP = models.CharField(max_length=20, default=None, null=True, verbose_name='电脑IP')
	# 设置时间字段为自动获取当前时间
	crDateTime = models.DateTimeField(auto_now=True,verbose_name='时间')
	crInfo = models.CharField(max_length=200,verbose_name='内容')
	crTopic = models.IntegerField(verbose_name='给谁留言')
	crType = models.IntegerField(verbose_name='类型')

	isDelete = models.BooleanField(default=False)
	# 使用自定义的管理表类
	crManager = MyManager()

	def getUser(self):
		return self.crUserId

	class Meta:
		db_table = 'chatRecords'

# 知识点回顾表
class Review(models.Model):
	'''作者、时间、主题、内容、地址、重要程度'''
	# 知识点回顾表与用户表是一对一的关系
	rUserId = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
	# 设置时间字段为自动获取当前时间
	rDateTime = models.DateTimeField(auto_now=True)
	rTopic = models.CharField(max_length=20)
	rInfo = models.CharField(max_length=200)
	rAddr = models.CharField(max_length=20)
	rImpo = models.CharField(max_length=20)
	isDelete = models.BooleanField(default=False)
	# 使用自定义的管理表类
	rManager = MyManager()

	class Meta:
		db_table = 'reviews'

# 博客类型
class BlogType(models.Model):
	''' 名称、简介'''
	bType = models.CharField(max_length=20, unique=True)
	bInfo = models.CharField(max_length=200)
	isDelete = models.BooleanField(default=False)

	# 使用自定义的管理表类
	bManager = MyManager()

	class Meta:
		# 自定义表名
		db_table = 'blogType'

# 博客信息表
class Blogs(models.Model):
	'''作者、时间、主题、内容、个人分类、文章类别、博客类型'''
	# 博客信息表与用户表是一对一的关系
	bUserId = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
	# 设置时间字段为自动获取当前时间
	bDateTime = models.DateTimeField(auto_now=True)
	bTopic = models.CharField(max_length=20)
	bInfo = models.CharField(max_length=200)
	bAddr = models.CharField(max_length=20)
	bPersonType = models.CharField(max_length=20)
	bArticleType = models.CharField(max_length=20)
	bBlogTypeId = models.ForeignKey(BlogType, on_delete=models.SET_NULL, blank=True, null=True)
	isDelete = models.BooleanField(default=False)
	# 使用自定义的管理表类
	bManager = MyManager()

	class Meta:
		db_table = 'blogs'

# 资料信息表
class DataBank(models.Model):
	'''作者、时间、主题、内容、类型、地址'''
	# 资料信息表与用户表是多对多的关系
	dUserId = models.ManyToManyField(User)
	# 设置时间字段为自动获取当前时间
	dDateTime = models.DateTimeField(auto_now=True)
	dTopic = models.CharField(max_length=20)
	dInfo = models.CharField(max_length=200)
	dAddr = models.CharField(max_length=20)

	isDelete = models.BooleanField(default=False)
	# 使用自定义的管理表类
	dManager = MyManager()

	class Meta:
		db_table = 'dataBank'

