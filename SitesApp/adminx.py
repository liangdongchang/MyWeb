
from xadmin import views
import xadmin
from .models import VoteType, User, Candidate, VoteRecord, ChatRecord, Review, BlogType, Blogs, DataBank

# 基础设置
class BaseSetting(object):
    enable_themes = True    # 使用主题
    use_bootswatch = True


# 全局设置
class GlobalSettings(object):
    site_title = '个人网站管理系统'  # 标题
    site_footer = '个人网站'  # 页尾
    site_url = '/'
    menu_style = 'accordion'  # 设置左侧菜单  折叠样式

# 用户的后台管理
class UserAdmin(object):
    # 检索字段
    search_fields = ['uName','uIP',]
    # 要显示的字段
    list_display = ['id','uName','uIP' ,'uEmail' ,'uNickName' ,'uGender','uAge' ,'uIcon' ,'isDelete']
    # 分组过滤的字段
    list_filter = ['uName','uNickName','uGender','uAge','isDelete']
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('id',)
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50
    # list_editable 设置默认可编辑字段
    list_editable = ['uNickName', 'uIcon']

# 投票类型的后台管理
class VoteTypeAdmin(object):
    # 检索字段
    search_fields = ['vType','isDelete']
    # 要显示的字段
    list_display = ['id','vType','vInfo','isDelete',]

    # 分组过滤的字段
    list_filter = ['vType','isDelete',]

# 候选者的后台管理
class CandidateAdmin(object):
    # 检索字段
    search_fields = ['cName','cAge','cTimes','cVotes','cPinyin','isDelete',]
    # 要显示的字段
    list_display = ['id','cName','cAge','cEmail','cDeclaration','cIcon','cTimes','cVotes','cPinyin','isDelete','cVoteType',]
    # 分组过滤的字段
    list_filter = ['cName','cAge','cTimes','cVotes','cPinyin','isDelete',]
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('id',)
    # fk_fields 设置显示外键字段
    fk_fields = ('cVoteType',)

# 投票记录的后台管理
class VoteRecordAdmin(object):
    # 检索字段
    search_fields = ['vUserId','vDate','vCandidateId','vComIP','vTypeId','vPolls','vTimes','isDelete']
    # 要显示的字段
    list_display = ['id','vUserId','vDate','vCandidateId','vComIP','vTypeId','vPolls','vTimes','isDelete']
    # 分组过滤的字段
    list_filter = ['vUserId','vDate','vCandidateId','vComIP','vTypeId','vPolls','vTimes','isDelete']

# 聊天记录的后台管理
class ChatRecordAdmin(object):
    # 检索字段
    search_fields = ['crUserId','crNickName','crIP','crDateTime','crInfo','crTopic','crType','isDelete']
    # 要显示的字段
    list_display = ['id','crUserId','crNickName','crIP','crDateTime','crInfo','crTopic','crType','isDelete']
    # 分组过滤的字段
    list_filter = ['crUserId','crNickName','crIP','crDateTime','crInfo','crTopic','crType','isDelete']

# 事项表的后台管理
class ReviewAdmin(object):
    # 检索字段
    search_fields = ['rUserId', 'rcDateTime', 'rmDateTime', 'rTopic', 'rImpo', 'isDelete']
    # 要显示的字段
    list_display = ['id', 'rUserId', 'rcDateTime', 'rmDateTime', 'rTopic', 'rContent', 'rImpo', 'rRemark', 'isDelete']
    # 分组过滤的字段
    list_filter = [ 'rUserId', 'rcDateTime', 'rmDateTime', 'rTopic',  'rImpo',  'isDelete']

xadmin.site.register(views.CommAdminView,GlobalSettings)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(VoteType, VoteTypeAdmin)
xadmin.site.register(User,UserAdmin)
xadmin.site.register(Candidate,CandidateAdmin)
xadmin.site.register(VoteRecord,VoteRecordAdmin)
xadmin.site.register(ChatRecord,ChatRecordAdmin)
xadmin.site.register(Review,ReviewAdmin)
xadmin.site.register(BlogType)
xadmin.site.register(Blogs)
xadmin.site.register(DataBank)






